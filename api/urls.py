from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/<slug>/', PostDetailView.as_view(), name='post-detail'),

]

