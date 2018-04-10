# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','category','excerpt')
    search_fields = ('title','author')
    list_filter = ('category','tags')
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)



