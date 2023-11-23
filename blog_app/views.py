from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.

def home(request):
    context = {

    }
    return render(request, 'blog_app/index.html', context)


def blogs(request):
    posts = Post.objects.select_related('author', 'category').all()
    context = {
        'posts': posts
    }
    return render(request, 'blog_app/blog.html', context)


def get_blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    context = {
        'post': post
    }
    return render(request, 'blog_app/post.html', context)


def get_category_posts(request, category_name):
    posts = Post.objects.select_related('author', 'category').filter(category__text=category_name)
    context = {
        'category': category_name,
        'posts': posts
    }
    return render(request, 'blog_app/filtered_post.html', context)


def services(request):
    return render(request, 'blog_app/services.html')


def about_us(request):
    return render(request, 'blog_app/about.html')


def contact(request):
    return render(request, 'blog_app/contact.html')