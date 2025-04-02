"""
Context processor for adding public chat rooms to base template.
"""
from src.chat.models import ChatRoom

def public_chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    return {"chat_rooms": chat_rooms}
