from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from posts.models import Post

from posts.serializers import (
    PostSerializer,
    NestedUserSerializer,
    CommentSerializer
)

User = get_user_model()

class NestedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'image', 'caption', 'liked_by', 'comments')

class PopulatedCommentSerializer(CommentSerializer):
    owner = NestedUserSerializer()

class UserSerializer(serializers.ModelSerializer):
    posts_made = NestedPostSerializer(many=True)
    followed_by = NestedUserSerializer(many=True)
    following = NestedUserSerializer(many=True)
    class Meta:
        model=User
        fields='__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'does not match'})

        # try:
        #     validation.validate_password(password=password)
        # except ValidationError as err:
        #     raise ValidationError({'password': err.messages})

        data['password'] = make_password(password)

        return data


    class Meta:
        model = User
        fields ='__all__'

class PopulatedPostSerializer(PostSerializer):
    comments = PopulatedCommentSerializer(many=True, read_only=True)
    liked_by = NestedUserSerializer(many=True, read_only=True)
    owner = UserSerializer()

class NestedPopulatedUserSerializer(UserSerializer):
    following = NestedUserSerializer(many=True)

class PopulatedUserSerializer(serializers.ModelSerializer):
    posts_made = PopulatedPostSerializer(many=True)
    following = NestedPopulatedUserSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    posts_made = PopulatedPostSerializer(many=True)
    # images_made = ImageSerializer(many=True)
    comments_made = CommentSerializer(many=True)
    liked_posts = NestedPostSerializer(many=True)
    followed_by = NestedUserSerializer(many=True)
    following = PopulatedUserSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
