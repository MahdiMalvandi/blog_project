from django.urls import path
from . import views
app_name = 'blog_app'
urlpatterns = [
    # pages
    path('', views.home, name='home'),
    path('blogs/', views.blogs, name='blogs'),
]