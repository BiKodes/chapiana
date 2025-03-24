"""Chapiana chat helpers."""
from channels.db import database_sync_to_async
from django.utils import timezone
import pycountry

from src.accounts.models import ChapianaUser
from src.chat.models import Message

def get_country_name_choices():
    """
    Gives a sorted list of tuples (country_code, country_name).
    """
    countries = [(country.alpha_2, country.name) for country in pycountry.countries]
    return sorted(countries, key=lambda x: x[1])

def get_country_code_by_name(country_name):
    """
    Gives the ISO Alpha-2 country code given a country name.
    """
    country = pycountry.countries.get(name=country_name)
    if country:
        return country.alpha_2
    
    # If direct lookup fails
    matches = [c for c in pycountry.countries if country_name.lower() in c.name.lower()]
    if matches:
        return matches[0].alpha_2
    
    return None

@database_sync_to_async
def save_message(chat_room, sender_name, receiver_name, message):
    """
    An async function to save the message to the database
    """
    sender = ChapianaUser.objects.get(username=sender_name)
    recipient = ChapianaUser.objects.get(username=receiver_name)

    # Create a new message
    new_message = Message(
        chat_room=chat_room,
        sender=sender,
        recipient=recipient,
        message_content=message,
        time=timezone.now().time(),
        created_at=timezone.now,
        updated_at=timezone.now(),
        read=True
    )
    new_message.save()
