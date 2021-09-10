from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    bio = models.TextField(max_length=150)
    profile_image = models.CharField(max_length=300)
    is_private = models.BooleanField(default=False)
    followed_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='following',
        blank=True
    )  
