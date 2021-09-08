from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from .models import Post
from .serializers import PostSerializer

class PostListView(ListCreateAPIView):
    ''' List View for /characters INDEX CREATE'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailView(RetrieveUpdateDestroyAPIView):
    ''' Detail View for /characters/id SHOW UPDATE DELETE'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
