import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from useraccount.models import UserMessage, UserScore
from django.views.generic import ListView, DetailView
from post.models import Post, Category, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from pms.views import IndexView

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchiveView(IndexView):
    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'), 
                created_time__month=self.kwargs.get('month'))

class TagView(IndexView):

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                TocExtension(slugify=slugify),
                            ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post