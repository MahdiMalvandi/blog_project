from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('gn/', PostListViewGenerics.as_view(), name='index'),
    path('gn/<pk>/', PostDetailApiViewGenerics.as_view(), name='index'),
    path('<pk>/', PostDetailView.as_view(), name='post_detail'),
]
