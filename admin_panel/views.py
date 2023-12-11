from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from blog_app.models import *


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


# endregion


# region blogs views
def blogs_page(request):
    return


def blog_detail(request, slug):
    ...

# endregion


def profile(request):
    return render(request, 'admin_panel/profile.html')



def test(request):
    return get_object_or_404(User, id=123)