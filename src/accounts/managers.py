"""
Custom User Model Manager for Chapiana.

This module defines a custom user model manager, `ChapianaUserManager`,
which uses email as the unique identifier for authentication instead of
usernames.
"""

from django.contrib.auth.base_user import BaseUserManager


class ChapianaUserManager(BaseUserManager):
    """
    Custom user model manager for Chapiana where email is the unique identifier
    for authentication instead of usernames.

    This manager provides methods for creating regular users and superusers,
    ensuring that all required fields are validated and properly set.
    """

    def create_user(self, email, username, password, **extra_fields):
        """
        Create and save a regular user with the given email, username, and password.
        """
        if not email:
            raise ValueError("Chapiana users must have an email address")
        if not username:
            raise ValueError("Chapiana users must have a username")
        if not password:
            raise ValueError("Chapiana users must have a password")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a superuser with the given email, username, and password.
        """
        if not email:
            raise ValueError("Chapiana superusers must have an email address")
        if not username:
            raise ValueError("Chapiana superusers must have a username")
        if not password:
            raise ValueError("Chapiana superusers must have a password")

        user = self.create_user(
            email=email, username=username, password=password, **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
