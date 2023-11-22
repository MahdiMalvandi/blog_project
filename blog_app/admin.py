from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", ]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = []

admin.site.register(Category)