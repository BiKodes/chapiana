import json
import logging
from asgiref.sync import sync_to_async

from channels.auth import login, logout
from channels.generic.websocket import AsyncWebsocketConsumer

from src.chat.utils import save_message, new_message_query, clear_history_query
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

    async def receive_new_message(self, text_data=None, bytes_data=None):
        """
        Receive message from WebSocket.
        """
        text_data_json = json.loads(text_data)
        chat_room = text_data_json["chat_room"]
        sender = text_data_json["sender"]
        recipient = text_data_json["recipient"]
        file = text_data_json["file"]
        message = text_data_json["message_content"]

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
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
                "chat_room": chat_room,
                "receiver": recipient,
            }
        )

    async def clear_history(self, data):
        room_name = data.get("roomName", None)
        clear_history = await clear_history_query(room_name)

        if clear_history:
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat_message",
                "command": "clear_history",
            })

    # Receive message from room group
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
        if command == 'image' or command == 'new_message':
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat_message",
                "content": (
                    lambda content: data['result']['image'] if (command == 'image') else data['result']['content'])(
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



    @sync_to_async
    def save_message(self, message, chat_room, sender, recipient):
        Message.objects.create(
            message_content=message,
            sender=sender,
            recipient=recipient,
            chat_room=chat_room
        )
