from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib.auth import login, authenticate, logout
from .models import *


# Create your views here.
def get_all_category():
    return Category.objects.all()


def home(request):
    if request.GET.get('q'):
        post = get_object_or_404(Post, id=request.GET.get('q'))
        return redirect('blog_app:blog page', post.slug)
    context = {
        'categories': get_all_category(),
    }
    return render(request, 'blog_app/index.html', context)


def blogs(request):
    posts = Post.objects.select_related('author', 'category').all()
    context = {
        'posts': posts,
        'categories': get_all_category(),
    }
    return render(request, 'blog_app/blog.html', context)


def get_blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    similar_posts = Post.objects.select_related('author', 'category').filter(category=post.category).exclude(id=post.id)
    short_link = request.build_absolute_uri('/')[:-1] + f'?q={post.id}'
    comments = Comment.objects.select_related('user', 'post').filter(post=post, reply__post=None)

    context = {
        'post': post,
        'categories': get_all_category(),
        'similar_posts': similar_posts,
        'short_link': short_link,
        'comments': comments
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


def get_user_info(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'blog_app/user-profile.html', context=context)


def profile(request):
    return render(request, 'blog_app/dashboard.html')


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            login(request)
            return redirect('blog_app:home')
    else:
        form = SignUpForm()
    context = {
        'form': form
    }
    return render(request, 'forms/signup.html', context=context)



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            login(request)
            return redirect('blog_app:home')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'forms/signin.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('blog_app:home')
