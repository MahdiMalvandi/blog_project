# Generated by Django 4.2.7 on 2023-11-22 15:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0003_alter_post_body_alter_post_likes_alter_post_save'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='save',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='save',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_save', to=settings.AUTH_USER_MODEL),
        ),
    ]
