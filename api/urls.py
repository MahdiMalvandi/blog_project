from django.urls import path
from .views import *
urlpatterns = [
    path('posts/', all_posts, name='posts')
]