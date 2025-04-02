"""
This file is for routing to the consumer.
"""
from django.urls import path, re_path

from src.chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
