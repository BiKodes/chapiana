"""Accounts modules."""
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    """User profile setup."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_proifle")
    image = models.ImageField(default="default.jpg", upload_to="profile_pics") 

    def __str__(self):
        """String representation of the user."""
        return f"{self.user.username} profile."
    
    def save(self, *args, **kwargs):
        """We are using Pillow for resizing the image."""
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
