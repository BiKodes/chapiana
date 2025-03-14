"""Chat Symbolic Constants."""

from django.db import models

class VideoCallStatus(models.IntegerChoices):
    CONTACTING = 0, 'Contacting'
    NOT_AVAILABLE = 1, 'Not Available'
    ACCEPTED = 2, 'Accepted'
    REJECTED = 3, 'Rejected'
    BUSY = 4, 'Busy'
    PROCESSING = 5, 'Processing'
    ENDED = 6, 'Ended'