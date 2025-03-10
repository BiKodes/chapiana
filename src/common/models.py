"""Base objects."""
import uuid

from django.db import models

from src.accounts.models import ChapianaUser

class UploadedFile(models.Model):
    """File upload data layer."""
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(ChapianaUser, on_delete=models.CASCADE, verbose_name=_('Uploaded_by'))
