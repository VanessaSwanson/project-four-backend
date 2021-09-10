from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Image, Post, Comment
from .serializers import PostSerializer, CommentSerializer, ImageSerializer


# POSTS

class PostListView(ListCreateAPIView):
    ''' List View for /posts INDEX CREATE'''
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request):
        serialized_post = PostSerializer(data=request.data)
        print(serialized_post)
        print(request.user.id)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response(serialized_post.data)
        return Response(serialized_post.errors)

    def get(self, request):
        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data)

class PostDetailView(RetrieveUpdateDestroyAPIView):
    ''' Detail View for /posts/:postId SHOW UPDATE DELETE'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class PostLikeView(APIView):
    ''' Adds likes to characters or removes if already liked '''

    permission_classes = (IsAuthenticated, )

    def post(self, request, post_pk):
        try:
            post_to_like = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise NotFound()

        if request.user in post_to_like.liked_by.all():
            post_to_like.liked_by.remove(request.user.id)
        else:
            post_to_like.liked_by.add(request.user.id)

        serialized_post = PostSerializer(post_to_like)

        return Response(serialized_post.data, status=status.HTTP_202_ACCEPTED)


# IMAGES

class ImageListView(APIView):
    ''' List View for /posts/:postId/images CREATE images'''
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def post(self, request, post_pk):
        request.data['post'] = post_pk
        created_image = ImageSerializer(data=request.data)
        if created_image.is_valid():
            created_image.save()
            return Response(created_image.data, status=status.HTTP_201_CREATED)
        return Response(created_image.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class ImageDetailView(APIView):
    ''' DELETE COMMENT VIEW '''
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def delete(self, _request, **kwargs):
        image_pk = kwargs['image_pk']
        try:
            image_to_delete = Image.objects.get(pk=image_pk)
            image_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            raise NotFound(detail='Image Not Found')



# COMMENTS

class CommentListView(APIView):
    ''' List View for /posts/:postId/comments CREATE comments'''
    permission_classes = (IsAuthenticated, )

    def post(self, request, post_pk):
        request.data['post'] = post_pk
        created_comment = CommentSerializer(data=request.data)
        if created_comment.is_valid():
            created_comment.save()
            return Response(created_comment.data, status=status.HTTP_201_CREATED)
        return Response(created_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class CommentDetailView(APIView):
    ''' DELETE COMMENT VIEW '''
    permission_classes = (IsAuthenticated, )

    def delete(self, _request, **kwargs):
        comment_pk = kwargs['comment_pk']
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound(detail='Comment Not Found')
