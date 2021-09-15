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
        blank=True,
    )

class Message(models.Model):
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User,
        related_name='messages_made',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='messages_received',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.sender} - {self.receiver} - {self.created_at}'
