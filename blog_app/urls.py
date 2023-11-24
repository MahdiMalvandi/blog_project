from django.urls import path
from . import views
app_name = 'blog_app'
urlpatterns = [
    # pages
    path('', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<str:slug>/', views.get_blog_detail, name='blog page'),
    path('blogs/category/<str:category_name>/', views.get_category_posts, name='category posts'),

    path('services/', views.services, name='services'),
    path('about_us/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),



]