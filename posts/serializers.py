from rest_framework import serializers
from django.contrib.auth import get_user_model
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from taggit.models import Tag
from .models import Post, Image, Comment

User = get_user_model()

class TagSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Tag
        fields = '__all__'

class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

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

class PopulatedPostSerializer(PostSerializer):
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = NestedUserSerializer(many=True, read_only=True)
    owner = NestedUserSerializer()
    tags = TagSerializer(many=True, read_only=True)
