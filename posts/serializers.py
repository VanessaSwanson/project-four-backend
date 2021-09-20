from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image', 'followed_by')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PopulatedCommentSerializer(CommentSerializer):
    owner = NestedUserSerializer()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'

class NestedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'image', 'caption', 'liked_by', 'owner', 'comments', 'created_at')

class PopulatedUserSerializer(serializers.ModelSerializer):
    posts_made = NestedPostSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__'      

class PopulatedPostSerializer(PostSerializer):
    comments = PopulatedCommentSerializer(many=True, read_only=True)
    liked_by = NestedUserSerializer(many=True, read_only=True)
    owner = PopulatedUserSerializer()
