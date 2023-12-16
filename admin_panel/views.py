from django.contrib import messages
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from blog_app.models import *
from blog_app.views import show_post, make_paginator, add_comment_base_view
from .forms import *
from django.contrib.postgres.search import TrigramSimilarity
from blog_app.forms import AddCommentForm


# Create your views here.
def search(request):
    if 'query' in request.GET:

        query = request.GET.get('query')
        context = {
            'query': query,
        }
        form = SearchForm(data=request.GET)
        if form.is_valid():

            if request.GET.get('type') == 'user':
                results_by_username = User.objects.annotate(similarity=TrigramSimilarity('username', query)).filter(
                    similarity__gt=0.1)
                results_by_first_name = User.objects.annotate(similarity=TrigramSimilarity('first_name', query)).filter(
                    similarity__gt=0.1)
                results_by_last_name = User.objects.annotate(similarity=TrigramSimilarity('last_name', query)).filter(
                    similarity__gt=0.1)
                results_by_job = User.objects.annotate(similarity=TrigramSimilarity('job', query)).filter(
                    similarity__gt=0.1)
                results_by_email = User.objects.annotate(similarity=TrigramSimilarity('email', query)).filter(
                    similarity__gt=0.1)

                results = (
                        results_by_username | results_by_first_name | results_by_last_name | results_by_job | results_by_email).order_by(
                    "-similarity")
                context['users'] = results
                return render(request, 'admin_panel/users.html', context)
            elif request.GET.get('type') == 'blog':
                results_by_title = Post.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(
                    similarity__gt=0.2)
                results_by_description = Post.objects.annotate(
                    similarity=TrigramSimilarity('description', query)).filter(
                    similarity__gt=0.1)
                results_by_body = Post.objects.annotate(similarity=TrigramSimilarity('body', query)).filter(
                    similarity__gt=0.1)
                results = (results_by_title | results_by_body | results_by_description).order_by("-similarity")
                context['blogs'] = results
                return render(request, 'admin_panel/blog.html', context)


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
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect('admin_panel:profile')
    context = {
        'user': user,
    }
    return render(request, 'admin_panel/user-profile.html', context)


def edit_user(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect('admin_panel:profile')
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:users')
    form = AddUserForm(instance=user)
    context = {
        'form': form,
        'edit': True,
    }
    return render(request, 'admin_panel/add-user.html', context)


def delete_user(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('admin_panel:users')


def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:users')
    form = AddUserForm()
    context = {
        'form': form,
    }
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
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:blog detail', slug)
    form = AddBlogForm(instance=post)
    context = {
        'edit': True,
        'form': form,
    }
    return render(request, 'admin_panel/add-blog.html', context=context)


def delete_post(request, slug):
    get_object_or_404(Post, slug=slug).delete()
    messages.success(request, 'Blog deleted successfully')
    return redirect('admin_panel:blogs')


def add_post(request):
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('admin_panel:blogs')
    form = AddBlogForm()
    context = {
        'form': form,
    }
    return render(request, 'admin_panel/add-blog.html', context)


def delete_thumbnail_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.thumbnail.delete()
    return redirect('admin_panel:edit post', slug)

# endregion


def add_comment(request, slug):

    return add_comment_base_view(request, slug, 'admin_panel:blog detail')


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = AddCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:blog detail', comment.post.slug)
    form = AddCommentForm(instance=comment)
    context = {
            'edit': True,
            'form': form,
    }
    return redirect('admin_panel:blog detail', comment.post.slug)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    slug = comment.post.slug
    comment.delete()
    return redirect('admin_panel:blog detail', slug)


def profile(request):
    return render(request, 'admin_panel/profile.html')


def category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category_form = form.save(commit=False)
            category_form.author = request.user
            category_form.save()
            return redirect('admin_panel:category')
    form = AddCategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'admin_panel/category.html', context)


def edit_category(request, text):
    category_selected = Category.objects.get(text=text)


def delete_category(request, text):
    category_selected = Category.objects.get(text=text)


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
