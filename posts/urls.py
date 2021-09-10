from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostLikeView,
    CommentListView,
    CommentDetailView,
    # ImageListView,
    # ImageDetailView
)

urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('<int:post_pk>/like/', PostLikeView.as_view()),
    path('<int:post_pk>/comments/', CommentListView.as_view()),
    path('<int:post_pk>/comments/<int:comment_pk>/', CommentDetailView.as_view()),
    # path('<int:post_pk>/images/', ImageListView.as_view()),
    # path('<int:post_pk>/images/<int:image_pk>/', ImageDetailView.as_view()),
]
