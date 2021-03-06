from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    UserListView,
    UserDetailView,
    UserFollowView,
    EditProfileView,
    UserMessageCreateView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('users/', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('<int:pk>/edit/', EditProfileView.as_view()),
    path('<int:user_pk>/follow/', UserFollowView.as_view()),
    path('<int:receiver_pk>/message/', UserMessageCreateView.as_view())
]
