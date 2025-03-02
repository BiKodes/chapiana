"""
Test Module for Email Utility Functionality.

This module contains unit tests for the test task function, which is responsible for
sending authentication codes via email. 

The tests cover both successful and failure scenarios, ensuring that the function behaves 
as expected under various conditions.

The tests use mocking to isolate the function from external dependencies (e.g., Django's
`send_mail` and the logger) and verify that the correct behavior and logging occur.
"""

import logging
from unittest.mock import patch
import pytest
from django.core.mail import send_mail
from src.config.common import Common
from src.accounts.utils import send_email


class TestSendEmail:
    """
    Test class for the `send_email` task function.

    This class groups all test cases related to the `send_email` function, ensuring
    that the function handles both successful email sending and error scenarios correctly.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Fixture to set up mocks for all test methods.

        This fixture automatically mocks the `send_mail` task function and the logger
        before each test and cleans up after the test is complete.
        """
        self.mock_send_mail = patch("django.core.mail.send_mail").start()
        self.mock_logger = patch("src.accounts.email_module._LOGGER").start()
        yield
        patch.stopall()  # Stop all patches after the test

    def test_send_email_success(self):
        """
        Test that the `send_email` function sends an email successfully and logs the event.
        """
        # Mock the send_mail function to return successfully
        self.mock_send_mail.return_value = 1  # send_mail returns the number of emails sent

        # Call the function
        result = send_email(random_code=123456, user_email="bikocodes@gmail.com")

        # Assertions
        self.mock_send_mail.assert_called_once_with(
            subject="Authentication Code",
            message="Your authentication code is 123456.",
            from_email=Common.EMAIL_HOST_USER,
            recipient_list=["bikocodes@gmail.com"],
        )
        self.mock_logger.info.assert_called_once_with(
            "Authentication code sent successfully to bikocodes@gmail.com."
        )
        assert result is True

    def test_send_email_failure(self):
        """
        Test that the `send_email` task function logs an error and re-raises the exception
        when email sending fails.
        """
        # Mock the send_mail function to raise an exception
        self.mock_send_mail.side_effect = Exception("SMTP connection failed")

        # Call the function and expect an exception
        with pytest.raises(Exception, match="SMTP connection failed"):
            send_email(random_code=123456, user_email="bikocodes@gmail.com")

        # Assertions
        self.mock_send_mail.assert_called_once_with(
            subject="Authentication Code",
            message="Your authentication code is 123456.",
            from_email=Common.EMAIL_HOST_USER,
            recipient_list=["bikocodes@gmail.com"],
        )
        self.mock_logger.error.assert_called_once_with(
            "The authentication code was not sent to bikocodes@gmail.com. "
            "Error: SMTP connection failed",
            exc_info=True,
        )
