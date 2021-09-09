from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import models, Post, Image, Comment

User = get_user_model()

class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'tag')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PopulatedCommentSerializer(CommentSerializer):
    owner = NestedUserSerializer()

class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = NestedUserSerializer(many=True, read_only=True)
    owner = NestedUserSerializer()
    # tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields='__all__'
