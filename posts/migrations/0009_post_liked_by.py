# Generated by Django 3.2.7 on 2021-09-09 14:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0008_auto_20210909_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_characters', to=settings.AUTH_USER_MODEL),
        ),
    ]