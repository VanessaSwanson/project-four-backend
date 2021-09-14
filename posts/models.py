from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=True)
    caption = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=300)
    liked_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='liked_posts',
        blank=True
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='posts_made',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title} - {self.id}'


class Comment(models.Model):
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='comments_made',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.post} - {self.id}'
