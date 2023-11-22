from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# region users model
class User(AbstractUser):
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')
    profile = models.ImageField(upload_to='users_profile/', blank=True)
    bio = models.TextField(blank=True, null=True, max_length=1000)
    job = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f'{self.username}'


# endregion

# region category models
class Category(models.Model):
    text = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'


# endregion

# region post model
class Post(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField(blank=True, null=True, max_length=1000)
    author = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ForeignKey(User, related_name='user_like', on_delete=models.CASCADE)
    save = models.ForeignKey(User, related_name='user_save', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.title} by {self.author}'

    class Meta:
        ordering = ["-created"]


# endregion

# region comments model
class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'a comment for {self.post} by {self.author}'
# endregion


# region users model
# endregion
