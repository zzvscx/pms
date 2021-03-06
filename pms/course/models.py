#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.db import models

# Create your models here.
# from useraccount.models import User


class Academy(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'学院')
    admin = models.ForeignKey(
        'useraccount.User', null=True, blank=True, verbose_name=u'院长')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Department(models.Model):
    academy = models.ForeignKey(Academy, verbose_name=u'学院')
    name = models.CharField(max_length=64, verbose_name=u'系')
    admin = models.ForeignKey(
        'useraccount.User', null=True, blank=True, verbose_name=u'系主任')
    length = models.IntegerField(default=4, verbose_name=u'学制')
    train_direction = models.CharField(
        max_length=128, null=True, blank=True, verbose_name=u'培养方向')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=128, null=True,
                            blank=True, verbose_name=u'班级')
    gradeId = models.CharField(max_length=32, verbose_name=u'班号')
    department = models.ForeignKey(Department, verbose_name='系')


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'课程类名')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SchoolTerm(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'学年学期')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def now_schoolterm(cls):
        now = datetime.now()
        if now.month < 9:
            name = '{}-{} {}'.format(now.year-1, now.year, '2')
        else:
            name = '{}-{} {}'.format(now.year, now.year+1, '1')
        return cls.objects.get(name=name)


    @classmethod
    def add_schoolterm(cls):
        date_from = 2000
        for i in range(100):
            date_from += 1
            name = '{}-{}'.format(date_from, date_from+1)
            cls.objects.get_or_create(name=name+' 1')
            cls.objects.get_or_create(name=name+' 2')

WEEK_DAYS=(
    (u'周一', u'周一'),
    (u'周二', u'周二'),
    (u'周三', u'周三'),
    (u'周四', u'周四'),
    (u'周五', u'周五'),
    (u'周六', u'周六'),
    (u'周日', u'周日'),
)

LESSON_CHOICE=(
    ('1-2','1-2'),
    ('3-4', '3-4'),
    ('5-6', '5-6'),
    ('7-8', '7-8'),
    (u'night', u'night'),
    )

class Schedule(models.Model):
    week_day = models.CharField(max_length=2,choices=WEEK_DAYS)
    lesson = models.CharField(max_length=3,choices=LESSON_CHOICE)
    
    def __unicode__(self):
        return '{} {}'.format(self.week_day, self.lesson)

    def __str__(self):
        return '{} {}'.format(self.week_day, self.lesson)
    
    @classmethod
    def add_schedule(cls):
        for i in WEEK_DAYS:
            for j in LESSON_CHOICE:
                cls.objects.create(week_day=i[0],lesson=j[0])

class ClassSchedule(models.Model):
    course = models.ForeignKey("Course")
    schedule = models.ForeignKey(Schedule)
    classroom = models.CharField(max_length=32, null=True, blank=True)
    def __unicode__(self):
        return '{}'.format(self.course.name)

    def __str__(self):
        return '{}'.format(self.course.name)

    @classmethod
    def sort(cls, class_schedule):
        res = {}
        for cs in class_schedule:
            res[cs.schedule.__str__()] = cs
        return res




class Course(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'课程名')
    code = models.CharField(max_length=32, verbose_name=u'课程代码')
    numbering = models.CharField(max_length=32, verbose_name=u'课程序号')
    category = models.ForeignKey(Category, verbose_name=u'课程类别')
    admin = models.ManyToManyField('useraccount.User', verbose_name=u'任课教师')
    school_term = models.ForeignKey(SchoolTerm, verbose_name=u'学年学期')
    total_score = models.IntegerField(default=100, verbose_name=u'总分')
    credit = models.FloatField(verbose_name=u'学分')
    midterm = models.FloatField(
        default=0, verbose_name=u'期中考试比例', help_text=u'按小数填写，如 0.1')
    final_exam = models.FloatField(
        default=1, verbose_name=u'期末考试比例', help_text=u'按小数填写，如 0.1')
    usual = models.FloatField(
        default=0, verbose_name=u'平时成绩比例', help_text=u'按小数填写，如 0.1')
    experimental = models.FloatField(
        default=0, verbose_name=u'实验成绩比例', help_text=u'按小数填写，如0.1')
    desc = models.TextField(null=True, blank=True, verbose_name=u'备注')
    created_at = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)

    @property
    def all_admin():
        res = ''
        for a in admin.all():
            res += a.name
        return res

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
