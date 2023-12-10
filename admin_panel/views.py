from django.shortcuts import render, HttpResponse
from blog_app.models import *

# Create your views here.

def home(request):
    users_count = User.objects.count()
    blogs_count = Post.objects.count()
    context = {
        'users_count': users_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'admin_panel/index.html', context)
