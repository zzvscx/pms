#-*- coding: utf-8 -*-
import urllib
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, Sum, Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import User, UserScore
from course.models import Course
from lib.excel import generate_xls_multisheet
# Create your views here.


class StudentBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(stuId=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/index/')

    if request.method == 'GET':
        return render(request, 'useraccount/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            return render(request, 'useraccount/login.html', {'error_message': u'账号或密码错误，请重新登录！'})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def user_detail(request):
    user = request.user
    if not user:
        raise Http404
    return render(request, 'useraccount/user_detail.html', locals())


@login_required
def user_points(request):

    if request.method != 'GET':
        raise Http404

    userscores = UserScore.objects.filter(
        user=request.user).order_by('course__school_term')
    term_score = []
    for scores in userscores.values('course__school_term__name').annotate(
            count=Count('id'), sum_points=Sum('points'), avg_points=Avg('points')):
        term_score.append([scores['course__school_term__name'],
                           scores['count'], scores['sum_points'], scores['avg_points']])
    all_score = userscores.aggregate(
        sum_points=Sum('points'), avg_points=Avg('points'))
    all_score = [userscores.count(), all_score['sum_points'],
                 all_score['avg_points']]
    if request.GET.get('download', False):
        data = [[u'学年学期', u'门数', u'总学分', u'平均绩点'], ]
        data.extend(term_score)
        all_score.insert(0,u'在校汇总')
        data.append(all_score)
        all_data = [[u'学年学期', u'课程代码', u'课程编号', u'课程名称', u'课程类别', u'学分',
                     u'期中成绩', u'期末成绩', u'平时成绩', u'补考成绩', u'总评成绩', u'实验成绩', u'最终成绩', u'绩点'], ]
        for userscore in userscores:
            course = userscore.course
            all_data.append([course.school_term.name, course.code,
                             course.numbering, course.name, course.category.name, course.credit, userscore.midterm,
                             userscore.final_exam, userscore.usual, userscore.retest, userscore.total_score,
                             userscore.experimental, userscore.total_score, userscore.points])
        name = u'{}{}成绩清单.xls'.format(datetime.now().strftime(
            '%Y%m%d'), request.user.name or request.user.username)
        excel = generate_xls_multisheet([{'name': u'成绩列表', 'data': data}, {'name': u'成绩汇总', 'data': all_data}])
        response = HttpResponse(excel, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = u'attachment; filename=%s' % urllib.quote(name.encode('utf8'))
        return response
    return render(request, 'useraccount/achievement.html', locals())


@login_required
def courses(request):
    if not request.user.is_staff:
        raise Http404
    courses = Course.objects.filter(admin__in=[request.user,]).order_by('created_at')
    return render(request, 'useraccount/courses.html',locals())

@login_required
def course_detail(request,pk):
    if not request.user.is_staff:
        raise Http404
    course = Course.objects.get(admin=request.user,pk=pk)
    userscores = UserScore.objects.filter(course=course)
    print userscores
    return render(request,'useraccount/course_detail.html',locals())
    

