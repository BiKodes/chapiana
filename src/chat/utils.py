"""Chapiana chat helpers."""

import base64

from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.utils import timezone

from src.accounts.models import ChapianaUser
from src.chat.models import ChatRoom, Message, VideoCall


def file_fixer(file_data):
    format, filestr = file_data.split(";base64,")
    ext = format.split("/")
    data = ContentFile(base64.b64decode(filestr), name="image")
    return data


@database_sync_to_async
def save_message(
    chat_room, sender_name, receiver_name, message=None, file=None
):
    """
    An async function to save the message to the database
    """
    sender = ChapianaUser.objects.get(username=sender_name)
    recipient = ChapianaUser.objects.get(username=receiver_name)

    new_message = Message(
        chat_room=chat_room,
        sender=sender,
        recipient=recipient,
        message_content=message,
        time=timezone.now().time(),
        created_at=timezone.now,
        updated_at=timezone.now(),
        read=True,
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
        chat_room_message = Message.objects.filter(
            chat_room__room_name=room_name
        )
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
        file=file,
    )

    if file:
        data = file_fixer(file)
        message_obj.file.save("image.jpg", data)
        message_obj.save()
    return message_obj
