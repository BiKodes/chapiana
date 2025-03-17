"""Chat Symbolic Constants."""

from datetime import timedelta

from django.db import models
from django.utils import timezone

class VideoCallStatus(models.IntegerChoices):
    CONTACTING = 0, 'Contacting'
    NOT_AVAILABLE = 1, 'Not Available'
    ACCEPTED = 2, 'Accepted'
    REJECTED = 3, 'Rejected'
    BUSY = 4, 'Busy'
    PROCESSING = 5, 'Processing'
    ENDED = 6, 'Ended'
    MISSED = 7, 'Missed'

ETA_TIME = timezone.now() + timedelta(minutes=1)