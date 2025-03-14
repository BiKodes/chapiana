import os

from src.config.common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LOCAL(Common):
    DEBUG = True

    INSTALLED_APPS = Common.INSTALLED_APPS

    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
