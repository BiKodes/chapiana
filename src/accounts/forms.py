"""Forms for user registration and profile management in the accounts application."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from src.accounts.models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Form for user registration.

    This form allows new users to register by providing a username and password.
    It inherits from Django's built-in `UserCreationForm` and adds custom fields.
    """

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information.

    This form allows existing users to update their username, email, first name,
    and last name.
    """

    email = forms.EmailField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.

    This form allows users to update their profile image.
    """

    class Meta:
        model = Profile
        fields = ["image"]
