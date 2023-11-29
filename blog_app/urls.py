from django.urls import path
from . import views
app_name = 'blog_app'
urlpatterns = [
    # pages
    path('', views.home, name='home'),
    # blogs urls
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<str:slug>/', views.get_blog_detail, name='blog page'),
    path('blogs/category/<str:category_name>/', views.get_category_posts, name='category posts'),
    path('blogs/<str:slug>/delete/', views.post_delete, name='delete post'),
    path('blogs/<str:slug>/edit/', views.post_edit, name='edit post'),


    path('users/<str:username>/', views.get_user_info, name='user info'),
    path('profile/', views.profile, name='profile'),

    path('services/', views.services, name='services'),
    path('about_us/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='sign up'),
    path('logout/', views.logout_view, name='log out'),

    path('manage-posts/', views.manage_posts, name='manage posts'),

    path('add-post/', views.add_post, name='add post'),

    path('blogs/<str:slug>/comments/add/', views.add_comment, name='add comment'),

]