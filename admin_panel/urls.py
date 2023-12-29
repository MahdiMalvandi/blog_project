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
    path('add-user/', add_user, name='add user'),

    path('search/', search, name='search'),
    # blogs url
    path('blogs/', posts_page, name='blogs'),
    path('add-post/', add_post, name='add post'),
    path('blogs/<str:slug>/', post_detail, name='blog detail'),
    path('blogs/<str:slug>/edit/', edit_post, name='edit post'),
    path('blogs/<str:slug>/delete/', delete_post, name='delete post'),
    path('blogs/<str:slug>/delete/thumbnail/', delete_thumbnail_post, name='delete thumbnail post'),

    path('blogs/category/<str:category_text>/', posts_category, name='post category'),
    path('categories/', category, name='category'),
    path('categories/<str:text>/edit/', edit_category, name='edit category'),
    path('categories/<str:text>/delete/', delete_category, name='delete category'),

    path('blogs/<str:slug>/add-comment/', add_comment, name='add comment'),

    path('comments/<pk>/edit/', edit_comment, name='edit comment'),
    path('comments/<pk>/delete/', delete_comment, name='delete comment'),


    path('profile/', profile, name='profile'),
    path('profile/delete-profile/', delete_profile, name='delete profile'),
    path('rooms/', rooms, name='room'),
    path('rooms/<pk>', room_chat, name='room answer'),
    path('rooms/add/', add_room, name='add room'),
    path('rooms/close/<pk>', close_room, name='close room'),
    path('rooms/search/', search_room, name='search room'),
    path('rooms/answer/<pk>', answer_message, name='answer message'),

]


