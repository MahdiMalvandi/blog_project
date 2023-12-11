from django.urls import path, include
from .views import *

app_name = 'admin_panel'

urlpatterns = [
    path('', home, name='home page'),

    # users url
    path('users/', users_page, name='users'),
    path('users/<str:username>/', user_profile, name='user_page'),
    path('users/<str:username>/edit/', edit_user, name='edit user page'),
    path('users/<str:username>/delete/', delete_user, name='delete user'),

    # blogs url
    path('blogs/', blogs_page, name='blogs'),
    path('blogs/<str:slug>/', blog_detail, name='blog detail'),

    path('profile/', profile, name='profile'),
    path('test/', test)
]


