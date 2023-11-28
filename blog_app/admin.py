from django.contrib import admin
from .models import *



# Register your models here.

class CommentTabularInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    fields = ["title", "body", "thumbnail", "author", "slug", "category"]
    inlines = [
        CommentTabularInline
    ]


admin.site.register(Category)