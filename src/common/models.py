"""Base objects."""
import uuid

from celery import Task
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.accounts.models import ChapianaUser
from src.common.utils import user_directory_path


class UploadedFile(models.Model):
    """
    Model to store files uploaded by users.
    """
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(ChapianaUser, on_delete=models.CASCADE, verbose_name=_("Uploaded_by"), related_name='+', db_index=True)
    file = models.FileField(verbose_name=_("File"), blank=False, upload_to=user_directory_path)
    uploaded_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Upload date"))

    def __str__(self):
        return str(self.file.name)


class BaseRetryTask(Task):
    """Celery Retry Task."""
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 5, "countdown": 10}
    # Exponential backoff
    retry_backoff = True
    # Adds random jitter for better scaling
    retry_jitter = True
    default_retry_delay = 5
