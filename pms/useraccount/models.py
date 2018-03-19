#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from collections import OrderedDict

# Create your models here.
from django.contrib.auth.models import AbstractUser

AbstractUser._meta.get_field('email').null = True
AbstractUser._meta.get_field('email').blank = True
AbstractUser._meta.get_field('username').max_length = 36


class User(AbstractUser):
    name = models.CharField(default='',max_length=32,verbose_name=u'姓名') 
    stuId = models.CharField(max_length=32, verbose_name=u'学号/教职工编号')
    grade = models.ForeignKey('Grade',null=True,blank=True,max_length=32, verbose_name=u'班级')
    intake = models.DateField(verbose_name=u'入学时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Academy(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'学院')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name=u'院长')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Department(models.Model):
    academy = models.ForeignKey(Academy,verbose_name=u'学院')
    name = models.CharField(max_length=64, verbose_name=u'系')
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name=u'系主任')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Grade(models.Model):
    name = models.CharField(max_length=128,null=True,blank=True, verbose_name=u'班级')
    gradeId = models.CharField(max_length=32,verbose_name=u'班号')
    department = models.ForeignKey(Department,verbose_name='系')


class Course(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'课程名')
    admin = models.ManyToManyField(User, verbose_name=u'任课教师')
    total_points = models.IntegerField(default=100, verbose_name=u'总分')
    rate = models.IntegerField(default=100,verbose_name=u'考试成绩占比')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class UserScore(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    test_points = models.FloatField(verbose_name=u'考试成绩')
    extre_points = models.FloatField(verbose_name=u'平时分')

    @property
    def total_points(self):
        return (self.test_points * self.course.rate + 
                self.extre_points * (100-self.course.rate))/100


