import json
import logging
from asgiref.sync import sync_to_async

from channels.auth import login, logout
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.renderers import JSONRenderer

from src.chat.utils import save_message, new_message_query, clear_history_query, chat_room_icon_query, get_chat_room
from src.chat.models import Message

LOGGER = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Chapiana Consumer.
    
    A consumer does three things:

        1. Accepts connections.
        2. Receives messages from client.
        3. Disconnects when the job is done.
    """
    async def connect(self):
        """
        Connect to a chat room.
        """
        user = self.scope["user"]

        if user.is_authenticated:
            # Connect only if the user is authenticated
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            LOGGER.info(self.room_name, self.room_group_name)

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.send({"close": True})

    async def disconnect(self, close_code):
        """
        Disconnect from channel.
    
        Leave room group.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def new_message(self, data=None):
        """
        Receive message from WebSocket.
        """
        await self.chat_notification(data)
        data_json = json.loads(data)
        chat_room = data_json["chat_room"]
        sender = data_json["sender"]
        recipient = data_json["recipient"]
        file = data_json["file"]
        message = data_json["message_content"]

        new_message =  await new_message_query(sender, chat_room, message, file)
        # Remove Byte String
        result = eval(new_message)

        if file:
            context = {"command": "file", "result": result}
        else:
            context = {"command": "new_message", "result": result}

        # Save message to DB
        await save_message(chat_room, sender, recipient, message)

        # Send message to room group
        await self.send_to_chat_message(context)

    async def change_icon(self, data):
        username = data.get("username", None)
        room_name = data.get("roomName", None)
        file_data = data.get("file", None)
        change_room_icon = await chat_room_icon_query(room_name, file_data)
        room_icon_json = await self.room_icon_serializer(change_room_icon)
        result = eval(room_icon_json)

        context = {
            "command": "change_icon",
            "result": result
        }

        await self.send_to_chat_message(context)
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat_message",
            "command": "info",
            "content": {
                "type": "changeIcon",
                "message": f"{username} changed the room icon."
            }
        })

    async def clear_history(self, data):
        room_name = data.get("roomName", None)
        clear_history = await clear_history_query(room_name)

        if clear_history:
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat_message",
                "command": "clear_history",
            })

    async def message_serializer(self, query):
        serialized_message = MessageSerializer(query)
        message_json = JSONRenderer().render(serialized_message.data)
        return message_json
    
    async def room_icon_serializer(self, query):
        serialize_icon = ChatRoomSerializer(query)
        icon_json = JSONRenderer().render(serialize_icon.data)
        return icon_json

    async def chat_notification(self, data):
        room_name = data["roomName"]
        username = data["username"]
        message = data.get("message", None)
        file = data.get("file", None)
        chat_room = await get_chat_room(room_name)

        members_list = []
        for _ in chat_room.members.all():
            members_list.append(_.username)

        result = {
            "type": "chat_message",
            "content": message,
            "__str__": username,
            "room_name": room_name,
            "members_list": members_list,
        }

        if file:
            result["content"] = "file"

        await self.channel_layer.group_send("chat_listener", result)

    async def chat_message(self, event):
        message = event["message_content"]
        chat_room = event["chat_room"]
        sender = event["sender"]
        recipient = event["recipient"]
        message = event["message_content"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message_content": message,
            "sender": sender,
            "receipient": recipient,
            "chat_room": chat_room,
        }))

    async def send_to_chat_message(self, data):
        command = data.get('command')
        if command == 'file' or command == 'new_message':
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat_message",
                "content": (
                    lambda content: data['result']['file'] if (command == 'file') else data['result']['content'])(
                    command),
                "__str__": data['result']['__str__'],
                "created_at": data['result']['created_at'],
                'command': command,
            })

        elif command == 'change_icon':
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'content': data['result']['room_image'],
                'command': command,
            })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    commands = {
        'new_message': new_message,
        'change_icon': change_icon,
        'clear_history': clear_history,
    }



 
