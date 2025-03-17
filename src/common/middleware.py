
"""Middleware for Auto Tracking users online status based on requests."""
from django.utils import timezone

class ActiveChapianaUserMiddleware:
    """."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, "status"):
                request.user.status.is_online = True
                request.user.status.was_online = timezone.now()
                request.user.status.save(update_field=["is_online", "was_online"])

        response = self.get_response(request)
        return response
