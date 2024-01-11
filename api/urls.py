from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register(r'posts', PostViewSet)

urlpatterns = [
    # path('posts/', PostListView.as_view(), name='posts'),
    # path('posts/<slug>/', PostDetailView.as_view(), name='post-detail'),

]
urlpatterns += routers.urls

