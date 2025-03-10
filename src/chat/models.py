"""Chapiana data layers."""
from datetime import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from src.accounts.models import ChapianaUser, Profile
from src.chat.constants.symbolic_constants import VIDEO_CALL_STATUS

class ChatRoom(models.Model):
    creator = models.ForeignKey(ChapianaUser, on_delete=models.CASCADE, null=True, related_name='room_creator')
    room_name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField(ChapianaUser, related_name='rooms')
    room_image = models.ImageField(upload_to='room-image', blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.room_name)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.room_name)
        super(ChatRoom, self).save()

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, related_name='messages')
    sender = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        related_name='from_user',
        db_index=True,
        verbose_name=_("Author"),
    )
    recipient = models.ForeignKey(
        ChapianaUser,
        on_delete=models.CASCADE,
        related_name='to_user',
        db_index=True,
        verbose_name=_("Recipient"),
    )
    message_content = models.TextField(verbose_name=_('Text'), blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='image-message')
    date_added = models.DateTimeField(auto_now_add=True)
    profile_pic = models.OneToOneField(
        Profile
    )

    class Meta:
        ordering = ('date_added', )

    def __str__(self):
        return f"{self.author.username}: {self.message_content}"

class VideoCall(models.Model):
    caller = models.ForeignKey(ChapianaUser, on_delete=models.CASCADE, related_name='caller')
    receiver = models.ForeignKey(ChapianaUser, on_delete=models.CASCADE, related_name='receiver')
    status = models.PositiveSmallIntegerField(default=0)
    date_started = models.DateTimeField(default=datetime.now())
    date_ended = models.DateTimeField(default=datetime.now())
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def status_name(self):
        return VIDEO_CALL_STATUS[self.status]
    
    @property
    def video_call_duration(self):
        return self.date_ended - self.date_started
