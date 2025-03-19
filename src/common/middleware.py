
"""Middleware for Auto Tracking users online status based on requests."""
from django.utils import timezone

class ChapianaActiveUserMiddleware:
    """
    Middleware to track user activity on each request and mark them as online.
    It also updates their last seen time.
    """
    def __init__(self, get_response):
        """
        Initializes the middleware with the response handler.
        """
        self.get_response = get_response

    def __call__(self, request):
        """"
        Processes each HTTP request and updates the user's online status and last seen timestamp.
        """
        if request.user.is_authenticated:
            if hasattr(request.user, "status"):
                request.user.status.is_online = True
                request.user.status.was_online = timezone.now()
                request.user.status.save(update_field=["is_online", "was_online"])

        response = self.get_response(request)
        return response
