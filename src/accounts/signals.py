# Signals to automatically create and save a Profile when a User is created.

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
