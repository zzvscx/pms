#-*- coding: utf-8 -*-
from django import template
from django.db.models.aggregates import Count
from ..models import Post, Category,Tag

register = template.Library()

#获取最新的文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]

#将文章按月份归档
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

#类别
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)