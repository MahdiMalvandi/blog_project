from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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


    path('services/', views.services, name='services'),
    path('about_us/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='sign up'),
    path('logout/', views.logout_view, name='log out'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),

    path('manage-posts/', views.manage_posts, name='manage posts'),
    path('profile/', views.profile, name='profile'),
    path('add-post/', views.add_post, name='add post'),
    path('change-profile/', views.change_profile, name='change profile'),

    path('blogs/<str:slug>/comments/add/', views.add_comment, name='add comment'),

]