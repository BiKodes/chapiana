"""Celery app instantiation."""
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTING_MODULE", "src.config.common")

app = Celery("config")
app.config_from_object("django.conf.settings", namespace="CELERY")
app.autodiscover_tasks()
