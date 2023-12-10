from django.urls import path, include
from .views import *

app_name = 'admin_panel'

urlpatterns = [
    path('', home, name='home page')
]