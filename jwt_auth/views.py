from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView
)
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt


from .serializers import UserProfileSerializer, UserRegisterSerializer, UserSerializer
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