from django.contrib import admin
from .models import *



# Register your models here.


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", ]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    fields = ["title", "body", "thumbnail", "author", "slug"]


admin.site.register(Category)