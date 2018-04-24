#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models import Count,Case,When,Q
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from collections import OrderedDict
from course.models import Grade, Course
from datetime import datetime, timedelta

AbstractUser._meta.get_field('email').null = True
AbstractUser._meta.get_field('email').blank = True
AbstractUser._meta.get_field('username').max_length = 36

METHOD_CHOICES = (
    (0, u'普通全日制'),
    (1, u'非全日制')
)

EDUCATION_CHOICES = (
    (0, u'本科'),
    (1, u'硕士'),
    (2, u'博士'),
)

CAMPUS_CHOICES = (
    (0, u'渭水校区'),
    (1, u'本部'),
    (2, u'小寨校区'),
    (3, u'雁塔校区'),

)


class User(AbstractUser):
    name = models.CharField(null=True, blank=True,
                            max_length=32, verbose_name=u'姓名')
    sex = models.CharField(null=True, blank=True,
                           max_length=32, verbose_name=u'性别')
    stuId = models.CharField(max_length=32, null=True,
                             blank=True, verbose_name=u'学号/教职工编号')
    at_school = models.BooleanField(default=True, verbose_name=u'是否在校')
    have_roll = models.BooleanField(default=True, verbose_name=u'是否有学籍')
    roll_in_school = models.BooleanField(default=True, verbose_name=u'是否在籍')
    team = models.ForeignKey(
        Grade, null=True, blank=True, max_length=32, verbose_name=u'班级')
    intake = models.DateField(null=True, blank=True, verbose_name=u'入学时间')
    leave = models.DateField(null=True, blank=True, verbose_name=u'预毕业时间')
    method = models.IntegerField(
        default=0, choices=METHOD_CHOICES, verbose_name=u'学习形式')
    education = models.IntegerField(
        default=0, choices=EDUCATION_CHOICES, verbose_name=u'学历')
    term = models.CharField(max_length=16, null=True,
                            blank=True, verbose_name=u'所在年级')
    campus = models.IntegerField(
        default=0, choices=CAMPUS_CHOICES, verbose_name=u'所属校区')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username

    @property
    def leave_school_date(self):
        if self.intake and self.team.department:
            return datetime(year=self.intake.year + self.team.department.length, month=7, day=1).strftime('%Y-%m-%d')
        return ''

    @property
    def str_method(self):
        return METHOD_CHOICES[self.method][1]

    @property
    def str_education(self):
        return EDUCATION_CHOICES[self.education][1]

    @property
    def str_campus(self):
        return CAMPUS_CHOICES[self.campus][1]


class UserScore(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    midterm = models.FloatField(null=True, blank=True, verbose_name=u'期中成绩')
    final_exam = models.FloatField(null=True, blank=True, verbose_name=u'期末成绩')
    usual = models.FloatField(null=True, blank=True, verbose_name=u'平时成绩')
    experimental = models.FloatField(
        null=True, blank=True, verbose_name=u'实验成绩')
    retest = models.FloatField(null=True, blank=True, verbose_name=u'补考成绩')
    total_score = models.FloatField(null=True, blank=True, verbose_name=u'总分')
    points = models.FloatField(null=True, blank=True, verbose_name=u'绩点')

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

    @classmethod
    def sort_userscores(cls,userscores):
        return userscores.aggregate(
            good=Count(Case(When(total_score__gte=85, then=1))),
            good_first=Count(Case(When(total_score__gte=85, total_score__lt=90, then=1))),
            good_second=Count(Case(When(total_score__gte=90, total_score__lt=95, then=1))),
            good_third=Count(Case(When(total_score__gte=95, total_score__lt=100, then=1))),
            perfect=Count(Case(When(total_score=100, then=1))),
            normal=Count(Case(When(total_score__gte=60, total_score__lt=85, then=1))),
            normal_first=Count(Case(When(total_score__gte=60, total_score__lt=70, then=1))),
            normal_second=Count(Case(When(total_score__gte=70, total_score__lt=80, then=1))),
            normal_third=Count(Case(When(total_score__gte=80, total_score__lt=85, then=1))),
            failed=Count(Case(When(total_score__lt=60, then=1))),
            failed_first=Count(Case(When(total_score__gte=0, total_score__lt=20, then=1))),
            failed_second=Count(Case(When(total_score__gte=20, total_score__lt=40, then=1))),
            failed_third=Count(Case(When(total_score__gte=40, total_score__lt=60, then=1))),
            )


@receiver(pre_save,sender=UserScore)
def update_data(*args,**kwargs):
    instance = kwargs.get('instance')
    course = instance.course
    if instance.final_exam:
        if instance.retest:
            instance.total_score = instance.retest
        else:
            instance.total_score = (instance.midterm or 0) * course.midterm +\
                                    (instance.final_exam or 0) * course.final_exam +\
                                    (instance.usual or 0) * course.usual +\
                                    (instance.experimental or 0) * course.experimental
        instance.points = instance.total_score / course.total_score * course.credit
        

class UserMessage(models.Model):
    user = models.ForeignKey(User)
    message_type = models.CharField(max_length=16,verbose_name=u'反馈类型')
    message = models.CharField(max_length=256, verbose_name=u'反馈内容')