from django.db.models import Count
from django.shortcuts import render, HttpResponse
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
