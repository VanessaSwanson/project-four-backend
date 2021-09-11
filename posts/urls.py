from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostLikeView,
    CommentListView,
    CommentDetailView,
)

urlpatterns = [
    path('', PostListView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('<int:post_pk>/like/', PostLikeView.as_view()),
    path('<int:post_pk>/comment/', CommentListView.as_view()),
    path('<int:post_pk>/comment/<int:comment_pk>/', CommentDetailView.as_view()),
]
