import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from src.chat.utils import save_message

LOGGER = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    """Chapiana Consumer."""
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        LOGGER.info(self.room_name, self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Leave room group.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        Receive message from WebSocket.
        """
        text_data_json = json.loads(text_data)
        chat_room = text_data_json["chat_room"]
        sender = text_data_json["sender"]
        recipient = text_data_json["recipient"]
        message = text_data_json["message_content"]

        await save_message(chat_room, sender, recipient, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender
            }
        )

        # Receive message from room group
        async def chat_message(self, event):
            message = event["message"]
            sender = event["sender"]

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                "message": message,
                "sender": sender
            }))
