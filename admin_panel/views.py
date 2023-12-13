from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from blog_app.models import *
from blog_app.views import show_post, make_paginator


# Create your views here.


def home(request):
    users_count = User.objects.filter(is_superuser=False).count()
    blogs = Post.objects.all().order_by('-created')
    comments_count = Comment.objects.filter(reply=None).count()
    admins_count = User.objects.filter(is_superuser=True).count()
    most_active_users = User.objects.annotate(num_posts=Count('user_posts')).order_by('-num_posts')

    context = {
        'users_count': users_count,
        'blogs': blogs,
        'comments_count': comments_count,
        'admins_count': admins_count,
        'most_active_users': most_active_users,

    }
    return render(request, 'admin_panel/index.html', context)


# region users views
def users_page(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin_panel/users.html', context)


def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        if user == request.user:
            return redirect('admin_panel:profile')
    except User.DoesNotExist:
        user = None
    context = {
        'user': user,
    }
    return render(request, 'admin_panel/user-profile.html', context)


def edit_user(request, username):
    return


def delete_user(request, username):
    return


def add_user(request):
    context = {}
    return render(request, 'admin_panel/add-user.html', context)


# endregion


# region blogs views
def posts_page(request):
    blogs = Post.objects.select_related('author', 'category').all()
    context = {
        'blogs': make_paginator(request, blogs, 6),
    }
    return render(request, 'admin_panel/blog.html', context)


def post_detail(request, slug):
    return show_post(request, slug, 'admin_panel/blog-detail.html')


def edit_post(request, slug):
    # post = get_object_or_404(Post, slug=slug)
    # if request.method == 'POST':
    #     form = AddPostFormAdmin(request.POST, request.FILES, instance=post)
    #     if form.is_valid():
    #         form = form.save(commit=False)
    #         form.author = post.author
    #         form.save()
    #         return redirect('blog_app:manage posts')
    # form = AddPostFormAdmin(instance=post)
    # context = {
    #     'edit': True,
    #     'form': form,
    # }
    # return render(request, 'forms/add-post.html', context=context)
    ...


def delete_post(request, slug):
    ...


def add_post(request):
    context = {}
    return render(request, 'admin_panel/add-blog.html', context)


# endregion


def add_comment(request, slug):
    ...


def edit_comment(request, pk):
    ...


def delete_comment(request, pk):
    ...


def profile(request):
    return render(request, 'admin_panel/profile.html')


def category(request):
    context = {}
    return render(request, 'admin_panel/category.html', context)


def posts_category(request, category_text):
    blogs = Post.objects.select_related('category', 'author').filter(category__text=category_text)
    context = {
        'blogs': make_paginator(request, blogs, 6),
        'category': category_text,
    }
    return render(request, 'admin_panel/blog.html', context)


def ticket(request):
    context = {}
    return render(request, 'admin_panel/tickets.html', context)


def test(request):
    return get_object_or_404(User, id=123)
