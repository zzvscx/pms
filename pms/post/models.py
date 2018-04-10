# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from django.db import models
from useraccount.models import User
from django.urls import reverse
from django.utils.html import strip_tags

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(verbose_name=u'标题', max_length=70)
    body = models.TextField(verbose_name=u'内容')
    excerpt = models.CharField(verbose_name=u'文章摘要', blank=True, max_length=200)
    category = models.ForeignKey(Category, verbose_name=u'类型')
    tags = models.ManyToManyField(Tag, verbose_name=u'标签',blank=True)
    author = models.ForeignKey(User, verbose_name=u'作者')
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name=u'最后修改时间', auto_now=True)
    img = models.ImageField(verbose_name=u'配图',upload_to='post/',null=True, blank=True,help_text='1400*300')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Mate:
        ordering=['-created_time']

    @property
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            #strip_tags 删除html标记
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args,**kwargs)