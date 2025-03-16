"""Chapiana chat tasks."""
import logging

from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from src.common.base import BaseRetryTask

LOGGER = logging.getLogger(__name__)


@shared_task(bind=True,  base=BaseRetryTask)
def notify_video_call_users(self, call_id, caller_id, receiver_id, status, date_started, date_ended, duration_seconds):
    """
    Celery task to notify users about the video call status over channels.
    """
    LOGGER.info(f"Starting notification task for VideoCall ID {call_id}.")

    # WebSocket Notification
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

    LOGGING.info(f"Celery Notification sent to {caller_group_name} and {receiver_group_name}")

    caller_group = f"user_{caller_id}_calls"
    receiver_group = f"user_{receiver_id}_calls"

    try:
        async_to_sync(channel_layer.group_send)(caller_group, payload)
        async_to_sync(channel_layer.group_send)(receiver_group, payload)

        LOGGER.info(f"WebSocket notification sent to {caller_group} and {receiver_group}")

        LOGGER.info(f"Notification task for VideoCall ID {call_id} completed successfully!")

    except  Exception as ex:
        LOGGER.error(
            f"Error in notify_video_call_users task: {str(ex)}"
        )
        #  Celery autoretry will handle retrying
        raise self.retry(ex)
