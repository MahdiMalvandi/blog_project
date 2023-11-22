from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    context = {
        'user': request.user
    }
    return render(request, 'blog/index.html', context)

def blogs(request):
    posts = Post.objects.select_related('author', 'category').all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/blog.html',context)

