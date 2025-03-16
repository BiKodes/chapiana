"""Chapiana chat tasks."""
import logging

from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

LOGGING = logging.getLogger(__name__)


@shared_task
def notify_video_call_users(call_id, caller_id, receiver_id, status, date_started, date_ended, duration_seconds):
    """
    Celery task to notify users about the video call status over channels.
    """
    channel_layer = get_channel_layer()

    payload = {
        # Method name in the consumer
        "type": "video_call_status",
        "call_id": call_id,
        "caller_id": caller_id,
        "receiver_id": receiver_id,
        "status": status,
        "date_started": date_started,
        "date_ended": date_ended,
        "duration_seconds": duration_seconds,
    }

    # Notify caller
    caller_group_name = f"user_{caller_id}_calls"
    async_to_sync(channel_layer.group_send)(
        caller_group_name,
        payload
    )

    # Notify receiver
    receiver_group_name = f"user_{receiver_id}_calls"
    async_to_sync(channel_layer.group_send)(
        receiver_group_name,
        payload
    )

    LOGGING.info(f"Celery Notification sent to {caller_group_name} and {receiver_group_name}")
