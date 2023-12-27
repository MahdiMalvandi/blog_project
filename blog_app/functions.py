from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect

from blog_app.forms import AnswerForm
from blog_app.models import Post, Comment, Room, Message


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


def answer_message_base(request, pk, next_page):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            message = Message.objects.create(body=cd['body'], user=request.user, room=room)
            message.save()
            return redirect(next_page, pk=pk)