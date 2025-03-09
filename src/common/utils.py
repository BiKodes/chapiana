"""Chapiana general helpers."""

from django.db import models

def user_directory_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    return f"user_{instance.uploaded_by.pk}/{filename}"
