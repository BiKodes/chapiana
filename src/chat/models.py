"""Chapiana data layers."""
from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, SoftDeletableModel

from src.accounts.models import ChapianaUser, Profile
from src.common.base import UploadedFile
from src.chat.constants.symbolic_constants import VideoCallStatus, ETA_TIME
from src.chat.tasks import notify_video_call_users


class ChatRoom(models.Model):
    """
    Represents a chat room that can be created by a user, with multiple members
    and an optional shared file.
    """
    creator = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        null=True,
        related_name="created_rooms",
        verbose_name="Creator"
    )
    room_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Room Name"
    )
    members = models.ManyToManyField(
        ChapianaUser,
        related_name="chat_rooms",
        verbose_name="Members"
    )
    room_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.DO_NOTHING,
        related_name="chat_rooms",
        verbose_name="Attached File",
        blank=True,
        null=True
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Slug"
    )

    class Meta:
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"
        ordering = ["room_name"]

    def __str__(self):
        """
        Returns a string representation of the chat room.
        """
        return self.room_name

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate a slug 
        from the room name.
        """
        if not self.slug:
            self.slug = slugify(self.room_name)
        super().save(*args, **kwargs)

class Conversation(TimeStampedModel):
    """
    Model representing a dialog (conversation) between two users.
    """
    id = models.BigAutoField(primary_key=True, verbose_name=_("Id"))
    first_user = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        verbose_name=_("first_user"),
        related_name="+", 
        db_index=True
    )
    second_user = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        verbose_name=_("second_user"),
        related_name="+", 
        db_index=True
    )

    class Meta:
        unique_together = (("first_user", "second_user"), ("second_user", "first_user"))
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")

    def __str__(self):
        return _("Conversation between {} and {}").format(self.first_user_id, self.second_user_id)

    @staticmethod
    def conversation_exists(user_one: ChapianaUser, user_two: ChapianaUser) -> None:
        """
        Check if a conversation already exists between two users.
        """
        return Conversation.objects.filter(
            Q(first_user=user_one, second_user=user_two) | Q(first_user=user_two, second_user=user_one)
        ).first()

    @staticmethod
    def create_if_not_exists(user_one: ChapianaUser, user_two: ChapianaUser):
        """
        Create a new conversation between two users if it doesn't exist.
        """
        if not Conversation.conversation_exists(user_one, user_two):
            Conversation.objects.create(first_user=user_one, second_user=user_two)

    @staticmethod
    def get_conversations_for_user(user: ChapianaUser):
        """
        Retrieve all conversations for a given user.
        """
        return Conversation.objects.filter(
            Q(first_user=user) | Q(second_user=user)
        ).values_list('first_user__pk', 'second_user__pk')


class Message(models.Model):
    """
    Model representing a message exchanged between users in a conversation or chat room.
    """
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, related_name="chat_messages")
    sender = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        related_name="from_user",
        verbose_name=_("Sender"),
        db_index=True,
    )
    recipient = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        related_name="to_user",
        verbose_name=_("Recipient"),
        db_index=True,
    )
    message_content = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    file = models.ForeignKey(UploadedFile, related_name="message", on_delete=models.DO_NOTHING, verbose_name="File", blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    profile_pic = models.OneToOneField(
        Profile
    )
    read = models.BooleanField(verbose_name=_("Read"), default=False)

    # Managers
    all_objects = models.Manager()

    class Meta:
        ordering = ("date_added", )
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return f"{self.sender.username}: {self.message_content}"
    
    @staticmethod
    def get_unread_count_for_dialog_with_user(sender, recipient) -> int:
        """
        Get the count of unread messages in a conversation between two users.
        """
        return Message.objects.filter(sender_id=sender, recipient_id=recipient, read=False).count()
    

    @staticmethod
    def get_last_message_for_conversation(sender, recipient):
        """
        Get the latest message exchanged in a conversation between two users.
        """
        return Message.objects.filter(
            Q(sender_id=sender, recipient_id=recipient) | Q(sender_id=recipient, recipient_id=sender) \
            .select_related("sender", "recipient")[0]
        )

    def save(self, *args, **kwargs):
        """
        Override save to ensure dialog creation if not already present.
        """
        super(Message, self).save(*args, **kwargs)
        Conversation.create_if_not_exists(self.sender, self.recipient)


class VideoCall(models.Model):
    """
    Represents a video call session between two users (caller and receiver).
    Stores call status, timestamps, and duration.
    """
    caller = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        related_name="video_calls_made",
        verbose_name="Caller"
    )
    receiver = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        related_name="video_calls_received",
        verbose_name="Receiver"
    )
    status = models.PositiveSmallIntegerField(
        choices=VideoCallStatus.choices,
        default=VideoCallStatus.CONTACTING,
        verbose_name="Call Status"
    )
    date_started = models.DateTimeField(
        default=timezone.now,
        verbose_name="Start Time"
    )
    date_ended = models.DateTimeField(
        default=timezone.now,
        verbose_name="End Time"
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        verbose_name = "Video Call"
        verbose_name_plural = "Video Calls"
        ordering = ["-date_created"]

    def __str__(self):
        return f"Call from {self.caller} to {self.receiver} on {self.date_created.strftime('%Y-%m-%d %H:%M:%S')}"

    @property
    def status_name(self):
        """
        Returns the human-readable name of the call status.
        Assumes VIDEO_CALL_STATUS is a dict mapping integers to strings.
        """
        # Auto-generated by Django for 'status'
        return self.get_status_display()

    @property
    def video_call_duration(self):
        """
        Returns the duration of the video call as a timedelta.
        """
        return self.date_ended - self.date_started
    
    @property
    def duration_in_seconds(self):
        """
        Returns the call duration in seconds as an integer.
        """
        duration: timedelta = self.video_call_duration
        return int(duration.total_seconds())
    
    def notify_users(self):
        """
        Trigger Celery task to notify users asynchronously.
        """
        notify_video_call_users.apply_async(
            args=[
                self.id,
                self.caller.id,
                self.receiver.id,
                self.status_name,
                self.date_started.isoformat(),
                self.date_ended.isoformat(),
                self.duration_in_seconds
            ],
            eta=ETA_TIME
        )
    
    def is_accepted(self):
        """
        Returns True if the call was accepted.
        """
        return self.status == self.VideoCallStatus.ACCEPTED
    
    def is_rejected(self):
        """
        Returns True if the call was rejected.
        """
        return self.status == self.VideoCallStatus.REJECTED

    def is_busy(self):
        """
        Returns True if the receiver was busy.
        """
        return self.status == self.VideoCallStatus.BUSY
    
    def is_ended(self):
        """
        Returns True if the call has ended.
        """
        return self.status == self.VideoCallStatus.ENDED
    
    def is_contacting(self):
        """
        Returns True if the call is currently contacting the receiver.
        """
        return self.status == self.VideoCallStatus.CONTACTING
    
    def is_not_available(self):
        """
        Returns True if the receiver was not available.
        """
        return self.status == self.VideoCallStatus.NOT_AVAILABLE
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.notify_users()

