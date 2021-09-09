from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# POSTS

class PostListView(ListCreateAPIView):
    ''' List View for /posts INDEX CREATE'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailView(RetrieveUpdateDestroyAPIView):
    ''' Detail View for /posts/:postId SHOW UPDATE DELETE'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# COMMENTS

class CommentListView(APIView):
    ''' List View for /posts/:postId/comments CREATE comments'''

    def post(self, request, post_pk):
        request.data['post'] = post_pk
        created_comment = CommentSerializer(data=request.data)
        if created_comment.is_valid():
            created_comment.save()
            return Response(created_comment.data, status=status.HTTP_201_CREATED)
        return Response(created_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):
    ''' DELETE COMMENT VIEW '''

    def delete(self, _request, **kwargs):
        comment_pk = kwargs['comment_pk']
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound(detail='Comment Not Found')
