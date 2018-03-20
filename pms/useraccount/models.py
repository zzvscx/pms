#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from collections import OrderedDict
from course.models import Grade, Course

AbstractUser._meta.get_field('email').null = True
AbstractUser._meta.get_field('email').blank = True
AbstractUser._meta.get_field('username').max_length = 36


class User(AbstractUser):
    name = models.CharField(default='', null=True, blank=True,max_length=32, verbose_name=u'姓名')
    stuId = models.CharField(max_length=32, null=True, blank=True, verbose_name=u'学号/教职工编号')
    team = models.ForeignKey(
        Grade, null=True, blank=True, max_length=32, verbose_name=u'班级')
    intake = models.DateField(null=True, blank=True,verbose_name=u'入学时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class UserScore(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    midterm = models.FloatField(null=True, blank=True, verbose_name=u'期中成绩')
    final_exam = models.FloatField(null=True, blank=True, verbose_name=u'期末成绩')
    usual = models.FloatField(null=True, blank=True, verbose_name=u'平时成绩')
    experimental = models.FloatField(
        null=True, blank=True, verbose_name=u'实验成绩')
    retest = models.FloatField(null=True, blank=True, verbose_name=u'补考成绩')

    @property
    def total_points(self):
        if self.retest:
            return self.retest
        else:
            return (self.midterm or 0) * self.course.midterm +\
                (self.final_exam or 0) * self.course.final_exam +\
                (self.usual or 0) * self.course.usual +\
                (self.experimental or 0) * self.course.experimental
    @property
    def grade_point_average(self):
        return self.total_points / self.course.total_points * self.course.credit

