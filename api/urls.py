from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vs', PostViewSet, basename='vs')

urlpatterns = [
    # path('', PostListView.as_view(), name='index'),
    # path('gn/', PostListViewGenerics.as_view(), name='index'),
    # path('gn/<pk>/', PostDetailApiViewGenerics.as_view(), name='index'),
    # path('<pk>/', PostDetailView.as_view(), name='post_detail'),
]
