"""Chapiana chat helpers."""
import base64

from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.utils import timezone
import pycountry

from src.accounts.models import ChapianaUser
from src.chat.models import Message, ChatRoom, VideoCall

def file_fixer(file_data):
    format, filestr = file_data.split(";base64,")
    ext = format.split("/")
    data = ContentFile(base64.b64decode(filestr), name="image")
    return data

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
def save_message(chat_room, sender_name, receiver_name, message=None, file=None):
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

    if file:
        data = file_fixer(file)
        new_message.save("image.jpg", data)
        new_message.save()
    return new_message

@database_sync_to_async
def chat_room_icon_query(room_name, file_data):
    chat_room = ChatRoom.objects.get(room_name=room_name)
    image = file_fixer(file_data)
    chat_room.room_name.save("image.jpg", image)
    chat_room.save()
    return chat_room


@database_sync_to_async
def clear_history_query(room_name):
    try:
        chat_room_message = Message.objects.filter(chat_room__room_name=room_name)
        chat_room_message.delete()
        return True
    except:
        return False
    
@database_sync_to_async
def get_chat_room(room_name):
    return ChatRoom.objects.get(room_name=room_name)

@database_sync_to_async
def new_message_query(username, room_name, message=None, file=None):
    sender = ChapianaUser.objects.get(username=username)
    recipient = ChapianaUser.objects.get(username=username)
    chat_room = ChatRoom.objects.get(room_name=room_name)
    message_obj = Message.objects.create(
        chat_room=chat_room,
        sender=sender,
        recipient=recipient,
        message_content=message,
        time=timezone.now().time(),
        created_at=timezone.now,
        updated_at=timezone.now(),
        read=True,
        file=file
    )

    if file:
        data = file_fixer(file)
        message_obj.file.save("image.jpg", data)
        message_obj.save()
    return message_obj

