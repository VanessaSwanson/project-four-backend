from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=True)
    caption = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.id}'

class Image(models.Model):
    image_link = models.CharField(max_length=300)
    post = models.ForeignKey(
        Post,
        related_name='images',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.post} - {self.id}'

class Tag(models.Model):
    tag = models.CharField(max_length=50)
    post = models.ForeignKey(
        Post,
        related_name='tags',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.tag} - {self.post} - {self.id}'
