from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

routers.register(r'posts', PostViewSet)
routers.register(r'comments', CommentViewSet)

urlpatterns = [
    # path('posts/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('rooms/', RoomView.as_view(), name='rooms'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
urlpatterns += routers.urls

