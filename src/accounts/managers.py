"""
Custom User Model Manager for Chapiana.

This module defines a custom user model manager, `ChapianaUserManager`,
which uses email as the unique identifier for authentication instead of
usernames. 

It extends Django's `BaseUserManager` to provide methods for creating
regular users and superusers.

The manager ensures that email, username, and password are required fields
for user creation and provides additional functionality for handling user
permissions and roles.
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

        Args:
            email (str): The user's email address. Must be unique.
            username (str): The user's username. Must be unique.
            password (str): The user's password.
            **extra_fields: Additional fields to be saved with the user.

        Returns:
            User: The newly created user instance.

        Raises:
            ValueError: If email, username, or password is not provided.
        """
        if not email:
            raise ValueError("Chapiana users must have an email address")
        if not username:
            raise ValueError("Chapiana users must have a username")
        if not password:
            raise ValueError("Chapiana users must have a password")

        # Normalize the email address and create the user
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Required for supporting multiple databases
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a superuser with the given email, username, and password.

        Args:
            email (str): The superuser's email address. Must be unique.
            username (str): The superuser's username. Must be unique.
            password (str): The superuser's password.
            **extra_fields: Additional fields to be saved with the superuser.

        Returns:
            User: The newly created superuser instance.

        Raises:
            ValueError: If email, username, or password is not provided.
        """
        if not email:
            raise ValueError("Chapiana superusers must have an email address")
        if not username:
            raise ValueError("Chapiana superusers must have a username")
        if not password:
            raise ValueError("Chapiana superusers must have a password")

        # Create the superuser with elevated permissions
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
