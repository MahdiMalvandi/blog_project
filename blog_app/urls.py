from django.urls import path, reverse_lazy
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
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/<pk>', views.show_ticket, name='show ticket'),
    path('tickets/add/', views.add_ticket, name='add ticket'),
    path('tickets/answer/<pk>', views.answer_ticket, name='answer ticket'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='sign up'),
    path('logout/', views.logout_view, name='log out'),


    path('password-reset/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',success_url=reverse_lazy("blog_app:home")),
         name='password_reset_confirm'),
    path('account/password_change/', views.account_change_password, name='account_change_password'),

    path('manage-posts/', views.manage_posts, name='manage posts'),
    path('profile/', views.profile, name='profile'),
    path('add-post/', views.add_post, name='add post'),
    path('change-profile/', views.change_profile, name='change profile'),

    path('blogs/<str:slug>/comments/add/', views.add_comment, name='add comment'),

]
