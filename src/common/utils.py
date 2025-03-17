"""Chapiana general helpers."""

from django.db import models

def user_directory_path(instance, filename: str) -> str:
    """
    Generate the upload path for a user's uploaded files.
    
    File will be uploaded to MEDIA_ROOT/user_<id>/<filename>.
    """
    return f"user_{instance.uploaded_by.pk}/{filename}"

