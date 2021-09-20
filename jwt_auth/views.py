from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
)
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

from .serializers import (
    UserProfileSerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserEditSerializer,
    MessageSerializer)
User = get_user_model()



class UserListView(ListAPIView):
    ''' List View for /auth/users INDEX'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(RetrieveUpdateDestroyAPIView):
    ''' Detail View for /auth/:userId SHOW UPDATE DELETE'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserRegisterSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response(
                {'message': 'Registration Successful'},
                status=status.HTTP_201_CREATED
            )
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(username=username)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Unauthorized')

        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Unauthorized')

        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            { 'sub': user_to_login.id, 'exp': int(expiry_time.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({
            'token': token,
            'message': f'Welcome back {username}'
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        serialized_user = UserProfileSerializer(request.user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)


class EditProfileView(UpdateAPIView):
    ''' Detail View for /auth/:userId SHOW UPDATE DELETE'''
    permission_classes = (IsAuthenticated, )

    queryset = User.objects.all()
    serializer_class = UserEditSerializer


class UserFollowView(APIView):
    ''' Adds likes to characters or removes if already liked '''

    permission_classes = (IsAuthenticated, )

    def post(self, request, user_pk):
        try:
            user_to_follow = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise NotFound()

        if request.user in user_to_follow.followed_by.all():
            user_to_follow.followed_by.remove(request.user.id)
        else:
            user_to_follow.followed_by.add(request.user.id)

        serialized_user = UserSerializer(user_to_follow)

        return Response(serialized_user.data, status=status.HTTP_202_ACCEPTED)

class UserMessageCreateView(CreateAPIView):
    ''' List View for auth/receiver_pk/message/ CREATE'''
    permission_classes = (IsAuthenticated, )

    def post(self, request, receiver_pk):
        request.data['sender'] = request.user.id
        request.data['receiver'] = receiver_pk
        serialized_message = MessageSerializer(data=request.data)
        print(serialized_message)
        print(request.user.id)
        if serialized_message.is_valid():
            serialized_message.save()
            return Response(serialized_message.data, status=status.HTTP_201_CREATED)
        return Response(serialized_message.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
