from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *
from rest_framework.routers import DefaultRouter


from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Episyche Technologies",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



routers = DefaultRouter()
app_name = 'api'

routers.register(r'posts', PostViewSet, basename='posts')
routers.register(r'comments', CommentViewSet)
routers.register(r'categories', CategoriesViewSet)

urlpatterns = [
    # path('posts/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('rooms/', RoomView.as_view(), name='rooms'),
    path('user/<username>/', UserProfileView.as_view(), name='user profile'),
    path('posts/category/<category_text>/', CategoryPostsView.as_view(), name='posts'),
    path('posts/search/', SearchView.as_view(), name='posts search'),
    path('posts/<slug>/comments/', GetPostComments.as_view(), name='get posts comments'),
    path('rooms/<pk>/', AddMessage.as_view(), name='message'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
urlpatterns += routers.urls

