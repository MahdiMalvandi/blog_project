from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from .forms import *
from .models import *


# Create your views here.
def make_paginator(request, posts, count=12):
    paginator = Paginator(posts, count)
    page = request.GET.get("page") if request.GET.get('page') else 1
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = []
    except PageNotAnInteger:
        posts = paginator.page(1)
    return posts


def show_post(request, slug, template_name):
    post = get_object_or_404(Post, slug=slug)
    similar_posts = Post.objects.select_related('author', 'category').filter(category=post.category).exclude(
        id=post.id)
    short_link = request.build_absolute_uri('/')[:-1] + f'?q={post.id}'
    comments = Comment.objects.select_related('user', 'post').filter(post=post, reply__post=None)
    context = {
        'post': post,

        'similar_posts': similar_posts,
        'short_link': short_link,
        'comments': comments
    }
    return render(request, template_name, context)


def home(request):
    if request.GET.get('q'):
        post = get_object_or_404(Post, id=request.GET.get('q'))
        return redirect('blog_app:blog page', post.slug)

    most_popular_posts = Post.objects.select_related('author', 'category').annotate(
        avg_points=Avg('post_comments__point'), comments_count=Count('post_comments')).order_by('avg_points',
                                                                                                'comments_count')

    latest_posts = Post.objects.select_related('author', 'category').all().order_by('-created')
    context = {
        'most_popular_post': most_popular_posts[:1].first(),
        'popular_posts': most_popular_posts[1:5],
        'latest_posts': latest_posts[:4],
    }
    return render(request, 'blog_app/index.html', context)


def blogs(request):
    results = []
    query = ''
    if 'q' in request.GET:
        query = request.GET.get('q')
        form = SearchPostForm(data=request.GET)
        if form.is_valid():
            results_by_title = Post.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(
                similarity__gt=0.1)
            results_by_body = Post.objects.annotate(similarity=TrigramSimilarity('body', query)).filter(
                similarity__gt=0.1)
            results = (results_by_title | results_by_body).order_by("-similarity")

            context = {
                "posts": make_paginator(request, results),
                "query": query
            }
            return render(request, 'blog_app/filtered_post.html', context=context)
    posts = Post.objects.annotate(avg_points=Avg('post_comments__point')).select_related('author', 'category').order_by(
        'avg_points').all()

    if 'time' in request.GET:
        time = request.GET['time']
        if time == 'newest':
            posts = Post.objects.select_related('author', 'category').all().order_by('-created')
        elif time == 'oldest':
            posts = Post.objects.select_related('author', 'category').all().order_by('created')
        else:
            posts = []

    context = {
        'posts': make_paginator(request, posts),
    }
    return render(request, 'blog_app/blog.html', context)


def get_blog_detail(request, slug):
    return show_post(request, slug, 'blog_app/post.html')


def get_category_posts(request, category_name):
    posts = Post.objects.select_related('author', 'category').filter(category__text=category_name)
    context = {
        'category': category_name,
        'posts': make_paginator(request, posts)
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


@login_required(redirect_field_name='next_page')
def profile(request):
    return render(request, 'blog_app/dashboard.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
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

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                if request.GET.get('next_page'):
                    return redirect(request.GET.get('next_page'))
                if user.is_superuser:
                    return redirect('admin_panel:home page')
                return redirect('blog_app:home')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'forms/signin.html', context=context)


@login_required(redirect_field_name='next_page')
def logout_view(request):
    logout(request)
    return redirect('blog_app:home')


@login_required(redirect_field_name='next_page')
def manage_posts(request):
    user_posts = Post.objects.select_related('author', 'category').filter(author=request.user)
    context = {
        'posts': user_posts,
    }
    return render(request, 'blog_app/manage-posts-for-users.html', context=context)


@login_required(redirect_field_name='next_page')
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('blog_app:manage posts')


@login_required(redirect_field_name='next_page')
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = post.author
            form.save()
            return redirect('blog_app:manage posts')
    form = AddPostForm(instance=post)
    context = {
        'edit': True,
        'form': form,
    }
    return render(request, 'forms/add-post.html', context=context)


@login_required(redirect_field_name='next_page')
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_app:manage posts')
    form = AddPostForm()
    context = {
        'form': form,
    }
    return render(request, 'forms/add-post.html', context=context)


def add_comment_base_view(request, slug, redirect_reverse):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = AddCommentForm(data=request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({'message'})
    else:
        form = AddCommentForm()

    return redirect(redirect_reverse, slug)


@login_required(redirect_field_name='next_page')
def add_comment(request, slug):
    return add_comment_base_view(request, slug, 'blog_app:blog page')


@login_required(redirect_field_name='next_page')
def change_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog_app:profile')
    form = ChangeProfileForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'forms/change-profile.html', context=context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/email_template.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('blog_app:home')


@login_required(redirect_field_name='next_page')
def account_change_password(request):
    if request.method == 'POST':
        form = AccountChangePasswordForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

            # Update the user's session to prevent them from being logged out
            update_session_auth_hash(request, user)

            return redirect('blog_app:profile')
    else:
        form = AccountChangePasswordForm()

    context = {'form': form}
    return render(request, 'blog_app/account_change_password.html', context)
