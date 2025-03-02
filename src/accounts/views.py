"""
This module defines API viewsets for user authentication.
"""

from random import randint
from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from src.accounts.serializers import LoginSerializer
from src.accounts.models import (
    ChapianaUser,
    OneTimePassword,
)
from src.accounts.utils import send_email



class LoginViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for handling user authentication.

    Supports:
    - Retrieving authentication status.
    - Logging users in.
    """
    
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    def retrieve(self, request, pk=None):
        """
        Handles GET requests.

        If the user is authenticated, redirects to 'chat:lobby'.
        Otherwise, renders the login page.
        """
        if request.user.is_authenticated:
            return redirect('chat:lobby')
        return render(request, 'account_app/auth.html')

    def create(self, request, *args, **kwargs):
        """
        Handles user login.

        Expects 'username' and 'password' in the request data.

        Returns:
            - 200 OK with username on successful login.
            - 401 Unauthorized if authentication fails.
            - 400 Bad Request if username or password is missing.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({'status': 200, 'username': user.username}, status=status.HTTP_200_OK)

            return Response({'status': 401, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'status': 400, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for handling user logout.
    
    Supports:
    - Logging out an authenticated user.
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logs out the authenticated user and returns a success response.

        Returns:
            - 200 OK on successful logout.
        """
        logout(request)
        return Response({'status': 200, 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class RegisterViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling user registration and authentication check.
    """
    queryset = OneTimePassword.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    def create(self, request, *args, **kwargs):
        """
        Handles user registration.
        - Validates input data using RegisterSerializer.
        - Checks if the username or email already exists.
        - Sends an OTP email for verification.
        - Stores user registration data with an OTP token.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
                return Response({'status': 409, 'message': 'User already exists'}, status=status.HTTP_409_CONFLICT)

            random_code = randint(100000, 999999)
            email_sent = send_email.delay(random_code, data['email'])
            email_result = email_sent.get()

            if email_result:
                token = str(uuid4())
                OneTimePassword.objects.create(
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=data['password'],
                    code=random_code,
                    token=token,
                )
                return Response({'status': 200, 'token': token}, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 500,
                    'message': 'Service OTP encountered an error. Please try again. If the error is not resolved, contact support'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'status': 400, 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def check_authentication(self, request):
        """
        Checks if the user is authenticated.
        - Redirects authenticated users to the chat lobby.
        - Redirects unauthenticated users to the login page.
        """
        if request.user.is_authenticated:
            return redirect('chat:lobby')
        return redirect('account:login')


class OneTimePasswordViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for OTP verification and user creation.
    Supports:
    - Checking OTP validity.
    - Registering a new user upon successful OTP verification.
    """
    serializer_class = OneTimePasswordSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    @action(detail=False, methods=['get'])
    def verify(self, request):
        """
        Handles GET requests.

        Redirects authenticated users to 'chat:lobby'.
        Redirects unauthenticated users to the login page.
        """
        if request.user.is_authenticated:
            return redirect('chat:lobby')
        return redirect('account:login')

    def create(self, request, *args, **kwargs):
        """
        Handles OTP verification and user creation.

        Expects 'token' and 'code' in the request data.

        Returns:
            - 200 OK with username on successful verification and user creation.
            - 400 Bad Request if OTP is invalid or missing.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            code = serializer.validated_data['code']

            try:
                new_user = OneTimePassword.objects.get(token=token, code=code)
                user = ChapianaUser.objects.create_user(
                    username=new_user.username,
                    first_name=new_user.first_name,
                    last_name=new_user.last_name,
                    email=new_user.email,
                    password=new_user.password
                )
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                new_user.delete()
                return Response({'status': 200, 'username': user.username}, status=status.HTTP_200_OK)
            except OneTimePassword.DoesNotExist:
                return Response({'status': 400, 'message': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'status': 400, 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for handling password recovery.
    Supports:
    - Sending an OTP to the user's email.
    - Verifying the OTP and logging the user in.
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    def list(self, request):
        """
        Handles GET requests.

        Expects an 'email' parameter in the query string.
        If the email exists, sends an OTP and returns a token.

        Returns:
            - 200 OK with a token if OTP is sent successfully.
            - 400 Bad Request if the user is not found or no email is provided.
            - 500 Internal Server Error if OTP sending fails.
        """
        email = request.GET.get('email', None)
        if email:
            try:
                user = ChapianaUser.objects.get(email=email)
            except ChapianaUser.DoesNotExist:
                return Response({'status': 400, 'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            random_code = randint(100000, 999999)
            email_sent = send_email(random_code, email)
            if email_sent:
                token = str(uuid4())
                OneTimePassword.objects.create(
                    username=user.username,
                    email=user.email,
                    code=random_code,
                    token=token,
                )
                return Response({'status': 200, 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 500,
                    'message': 'Service OTP encountered an error. Please try again. If the error is not resolved, contact support'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'status': 400, 'message': 'Data not sent'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests for OTP verification.

        Expects 'token' and 'code' in the request data.
        If the OTP is correct, logs the user in and deletes the OTP record.

        Returns:
            - 200 OK with the username on successful verification.
            - 400 Bad Request if the OTP is incorrect or missing.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            code = serializer.validated_data['code']
            
            try:
                user_otp = OneTimePassword.objects.get(token=token, code=code)
                username = user_otp.username
            except OneTimePassword.DoesNotExist:
                return Response({'status': 400, 'message': 'Code is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            
            find_user = ChapianaUser.objects.get(username=username)
            login(request, find_user)
            user_otp.delete()
            return Response({'status': 200, 'username': username}, status=status.HTTP_200_OK)
        
        return Response({'status': 400, 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
