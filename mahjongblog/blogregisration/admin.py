# blog/admin.py
from django.contrib import admin
from .models import Post, Category
from django.contrib import admin
from django.utils.safestring import mark_safe

admin.site.register(Post)
admin.site.register(Category)
