#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

AbstractUser._meta.get_field('email').null = True
AbstractUser._meta.get_field('email').blank = True
AbstractUser._meta.get_field('username').max_length = 36


class User(AbstractUser):
    stuId = models.CharField(max_length=32,verbose_name=u'学号/教职工编号')

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username


