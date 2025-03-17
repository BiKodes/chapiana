"""Signals to Track Call Lifecycle Events."""
import logging

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from src.chat.models import VideoCall
from src.chat.constants.symbolic_constants import VideoCallStatus

LOGGER =logging.getLogger(__name__)

@receiver(pre_save, sender=VideoCall)
def track_status_change(sender, instance, **kwargs):
    """
    Track call status changes before saving.
    """
    if instance.pk:
        previous = VideoCall.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            LOGGER.info(
                f"Status changed from {previous.get_status_display()} to {instance.get_status_display()}"
            )
            previous.save()


@receiver(post_save, sender=VideoCall)
def call_lifecycle_handler(sender, instance, created, **kwargs):
    """
    Handle events after a call is saved.
    """
    if created:
        LOGGER.info(
            f"New call initiated between {instance.caller} and {instance.receiver}"
        )
        # Send notification on new call start
        instance.notify_users()

    elif instance.status == VideoCallStatus.ENDED:
        LOGGER.info(
            f"Call ended between {instance.caller} and {instance.receiver}"
        )
        # Notify about call ending
        instance.notify_users()
