from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

class LoginViewSet(viewsets.ViewSet):
    """
    A ViewSet for user login.

    GET

      - If the user is authenticated, redirects to the chat lobby.
      - Otherwise, renders the login (authentication) template.

    POST

      - Authenticates the user based on provided username and password.
      - On success, logs the user in and returns a success JSON response.
      - On failure, returns an appropriate error response.
    """

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def list(self, request):
        """
        Handles GET requests.

        If the user is authenticated, redirects to 'chat:lobby'.
        Otherwise, renders the 'account_app/auth.html' template.
        """
        if request.user.is_authenticated:
            return redirect('chat:lobby')
        return render(request, 'account_app/auth.html')

    def create(self, request):
        """
        Handles POST requests to authenticate and log in a user.

        Expects 'username' and 'password' in the request data.

        Returns:
            - 200 OK with username on successful login.
            - 401 Unauthorized if authentication fails.
            - 400 Bad Request if username or password is missing.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(
                    {'status': 200, 'username': user.username},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'status': 401}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'status': 400}, status=status.HTTP_400_BAD_REQUEST)
