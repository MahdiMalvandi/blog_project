from django.contrib import admin
from .models import *


class CommentTabularInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", 'pk']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    fields = ["title", "body", "thumbnail", "author", "slug", "category", "description"]
    inlines = [
        CommentTabularInline
    ]


class MessagesTabularInline(admin.TabularInline):
    model = Message
    extra = 0


admin.site.register(Category)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [
        MessagesTabularInline
    ]
