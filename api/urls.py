from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register(r'posts', PostViewSet)
routers.register(r'comments', CommentViewSet)

urlpatterns = [
    # path('posts/<slug>/', PostDetailView.as_view(), name='post-detail'),

]
urlpatterns += routers.urls

