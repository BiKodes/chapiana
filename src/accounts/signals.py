# Signals specifically meant for user(s).
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.accounts.models import ChapianaUser, Profile

@receiver(post_save, sender=ChapianaUser)
def create_profile(sender, instance, created, **kwargs):
    """Creates a Profile instance whenever a new User is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=ChapianaUser)
def save_profile(sender, instance, **kwargs):
    """Ensures the Profile instance is saved whenever the User is updated."""
    instance.profile.save()

@receiver(user_logged_in)
def handle_user_logged_in(sender, user, request, **kwargs):
    """
    Marks the user as online when they log in."
    """
    if hasattr(user, "status"):
        user.status.mark_online()

def handle_user_logged_out(sender, user, request, **kwargs):
    """
    Marks the user as offline and records the time when they log out."
    """
    if hasattr(user, "status"):
        user.status.mark_offline()
