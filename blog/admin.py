from django.contrib import admin
from .models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "title", "category__name"]


# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
