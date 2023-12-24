from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import TrigramSimilarity

from .forms import *
from .decorators import custom_permission_required

from blog_app.forms import AddCommentForm
from blog_app.views import show_post, make_paginator, add_comment_base_view


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
    return redirect('admin_panel:home page')


def home(request):
    users_count = User.objects.filter(is_superuser=False).count()
    blogs = Post.objects.all().order_by('-created')
    comments_count = Comment.objects.filter(reply=None).count()
    admins_count = User.objects.filter(is_superuser=True).count()
    most_active_users = User.objects.annotate(num_posts=Count('user_posts')).order_by('-num_posts')[:5]
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
    form = UserPermissionForm(user)

    if user == request.user:
        return redirect('admin_panel:profile')

    if not request.user.is_superuser:
        for field_name, field in form.fields.items():
            field.widget.attrs['disabled'] = True

    if request.method == 'POST':
        if request.user.is_staff or user == request.user:
            form = UserPermissionForm(user, data=request.POST)
            if form.is_valid():
                for key in form.cleaned_data:
                    permission_id = key.split('_')[1]
                    permission = Permission.objects.get(pk=permission_id)
                    if form.cleaned_data[key]:
                        user.user_permissions.add(permission)
                    else:
                        user.user_permissions.remove(permission)

    return render(request, 'admin_panel/user-profile.html', {'user': user, 'form': form})


# def user_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     if user == request.user:
#         return redirect('admin_panel:profile')
#     if user.is_superuser:
#         permissions = 'all'
#     else:
#         # Get the permissions
#         ...
#     context = {
#         'user': user,
#         'permissions':permissions
#     }
#     return render(request, 'admin_panel/user-profile.html', context)


def edit_user(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return redirect('admin_panel:profile')
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit User was successful')

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
    messages.success(request, 'The User was deleted successfully')
    return redirect('admin_panel:users')


def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The User was added successfully')

            return redirect('admin_panel:users')
    form = AddUserForm()
    context = {
        'form': form,
    }
    return render(request, 'admin_panel/add-user.html', context)


# endregion

# region blogs views
@custom_permission_required('blog_app.view_post', message='You Can not see this page')
def posts_page(request):
    blogs = Post.objects.select_related('author', 'category').all()

    context = {
        'blogs': make_paginator(request, blogs, 6),
    }
    return render(request, 'admin_panel/blog.html', context)


@custom_permission_required('blog_app.view_post', message='You Can not see post detail')
def post_detail(request, slug):
    return show_post(request, slug, 'admin_panel/blog-detail.html')


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Post was successful')

            return redirect('admin_panel:blog detail', slug)
    form = AddBlogForm(instance=post)
    context = {
        'edit': True,
        'form': form,
    }
    return render(request, 'admin_panel/add-blog.html', context=context)


def delete_post(request, slug):
    get_object_or_404(Post, slug=slug).delete()
    messages.success(request, 'The Post was deleted successfully')

    return redirect('admin_panel:blogs')


def add_post(request):
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'The Post was added successfully')

            return redirect('admin_panel:blogs')
    form = AddBlogForm()
    context = {
        'form': form,
    }
    return render(request, 'admin_panel/add-blog.html', context)


def delete_thumbnail_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.thumbnail.delete()
    messages.success(request, 'The Thumbnail of the post was deleted successfully')

    return redirect('admin_panel:edit post', slug)


def posts_category(request, category_text):
    blogs = Post.objects.select_related('category', 'author').filter(category__text=category_text)
    context = {
        'blogs': make_paginator(request, blogs, 6),
        'category': category_text,
    }
    return render(request, 'admin_panel/blog.html', context)


# endregion

# region comments views

def add_comment(request, slug):
    messages.success(request, 'The Comment was added successfully')
    return add_comment_base_view(request, slug, 'admin_panel:blog detail')


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = AddCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Comment was successful')
            return redirect('admin_panel:blog detail', comment.post.slug)
    form = AddCommentForm(instance=comment)
    context = {
        'edit': True,
        'form': form,
    }
    return render(request, 'admin_panel/edit-comments.html', context)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    slug = comment.post.slug
    messages.success(request, 'The Comment was deleted successfully')

    comment.delete()
    return redirect('admin_panel:blog detail', slug)


# endregion

# region category views

def category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category_form = form.save(commit=False)
            category_form.author = request.user
            category_form.save()
            messages.success(request, 'The Category was added successfully')

            return redirect('admin_panel:category')
    form = AddCategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'admin_panel/category.html', context)


def edit_category(request, text):
    category_selected = Category.objects.get(text=text)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category_selected)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edit Category was successful')

            return redirect('admin_panel:category')
    form = AddCategoryForm(instance=category_selected)
    context = {
        'form': form
    }
    return render(request, 'admin_panel/edit-category.html', context)


def delete_category(request, text):
    category_selected = Category.objects.get(text=text)
    category_selected.delete()
    messages.success(request, 'The Category deleted successfully')

    return redirect('admin_panel:category')


# endregion


def profile(request):
    return render(request, 'admin_panel/profile.html')


def tickets(request):
    all_tickets = Ticket.objects.select_related('user').filter(answer=None)
    context = {
        'tickets': all_tickets
    }
    return render(request, 'admin_panel/tickets.html', context)


def ticket_answer(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    other_tickets = Ticket.objects.select_related('user').filter(answer=None).exclude(pk=pk)

    context = {
        'other_tickets': other_tickets,
        'ticket': ticket
    }
    return render(request, 'admin_panel/ticket_page.html', context)


def close_ticket(request, pk):
    return