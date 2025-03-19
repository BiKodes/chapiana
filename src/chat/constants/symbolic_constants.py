"""Chat Symbolic Constants."""

from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


ETA_TIME = timezone.now() + timedelta(minutes=1)
class VideoCallStatus(models.IntegerChoices):
    CONTACTING = 0, 'Contacting'
    NOT_AVAILABLE = 1, 'Not Available'
    ACCEPTED = 2, 'Accepted'
    REJECTED = 3, 'Rejected'
    BUSY = 4, 'Busy'
    PROCESSING = 5, 'Processing'
    ENDED = 6, 'Ended'
    MISSED = 7, 'Missed'

class ChatType(models.TextChoices):
    """
    Defines types of chat available.
    """
    PRIVATE_MESSAGE = "PRIVATE_MESSAGE",_( "Private Message")
    GROUP_MESSAGE = "GROUP_MESSAGE", _("Group Room")

class ChapianaUserPackage(models.TextChoices):
    """
    Defines user subscription packages.
    """
    FREE = "FREE", _("Free")
    PAID = "PAID", _("Paid")

