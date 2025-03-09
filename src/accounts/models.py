"""
Accounts Module for Chapiana.

This module defines the custom user model `ChapianaUser`, the `Profile` model
for user profiles, and the `OneTimePassword` model for handling one-time password
(OTP) functionality.
"""

from django.db import models
from django.contrib.auth.models import(
    AbstractUser,
    Group,
    Permission
)
from PIL import Image

from src.accounts.managers import ChapianaUserManager


class ChapianaUser(AbstractUser):
    """
    Custom user model for Chapiana.
    """

    groups = models.ManyToManyField(
        Group,
        related_name="chapianauser_groups_set",
        blank=True,
        help_text="The groups this user belongs to.",
        related_query_name="chapianauser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="chapianauser_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="chapianauser",
    )

    email = models.EmailField(unique=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = ChapianaUserManager()

    def __str__(self):
        """String representation of the user."""
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    """
    User profile model for Chapiana.

    It handles user profile information, including profile images.
    It uses the Pillow library to resize images upon saving.
    """

    user = models.OneToOneField(
        ChapianaUser,
        on_delete=models.CASCADE,
        related_name="user_profile"
    )
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        """String representation of the profile."""
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        """
        Save the profile and resize the profile image if necessary.

        This method overrides the default `save` method to resize the profile image
        using the Pillow library if the image dimensions exceed 300x300 pixels.
        """
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class OneTimePassword(models.Model):
    """
    One-Time Password (OTP) model for Chapiana.

    This model is used for OTP-based authentication and user registration.
    It stores temporary user information, including username, email, and OTP details.
    """

    username = models.CharField(max_length=150)
    email = models.EmailField()
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=60, null=True, blank=True)
    code = models.SmallIntegerField()
    token = models.CharField(max_length=125)

    def __str__(self):
        """String representation of the OTP instance."""
        return self.username
