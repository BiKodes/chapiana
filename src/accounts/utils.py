"""
Email Utility Module for Chapiana.

This module provides functionality for sending authentication codes via email.
It uses Django's `send_mail` function to send emails and Celery's `shared_task`
decorator to handle the task asynchronously. Logging is implemented to track
the success or failure of email delivery.
"""

import logging
from logging import Logger
from typing import Final

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

# Initialize logger
_LOGGER: Final[Logger] = logging.getLogger(__name__)


@shared_task
def send_email(random_code: int, user_email: str) -> bool:
    """
    Send an authentication code to the user's email address.

    This function sends an email containing the authentication code to the specified
    email address. It logs any errors that occur during the email sending process.
    """
    try:
        send_mail(
            subject="Authentication Code",
            message=f"Your authentication code is {random_code}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
        )
        _LOGGER.info(f"Authentication code sent successfully to {user_email}.")
        return True
    except Exception as exc:
        _LOGGER.error(
            f"The authentication code was not sent to {user_email}. Error: {exc}",
            exc_info=True,
        )
        # Re-raise the exception to ensure the task is marked as failed
        raise
