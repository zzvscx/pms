#-*- coding: utf-8 -*-
import xlrd
import urllib
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, Sum, Avg, Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from .models import User, UserScore
from course.models import Course, ClassSchedule, SchoolTerm
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
def change_password(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'useraccount/change_pw.html')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')
        print new_password, re_password
        print old_password, user.password
        if not auth.authenticate(username=user.username, password=old_password):
            err_msg = u'原密码输入错误' 
        elif new_password != re_password:
            err_msg = u'两次新密码输入不一致'
        else:
            return HttpResponse('密码修改成功！')
        return render(request, 'useraccount/change_pw.html',locals())

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
                 '%.3f'%all_score['avg_points']]
    if request.GET.get('download', False):
        data = [[u'学年学期', u'门数', u'总学分', u'平均绩点'], ]
        data.extend(term_score)
        all_score.insert(0, u'在校汇总')
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
        excel = generate_xls_multisheet([{'name': u'成绩列表', 'data': data}, {
                                        'name': u'成绩汇总', 'data': all_data}])
        response = HttpResponse(excel, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = u'attachment; filename=%s' % urllib.quote(
            name.encode('utf8'))
        return response
    return render(request, 'useraccount/achievement.html', locals())


@login_required
def courses(request):
    if not request.user.is_staff:
        raise Http404
    courses = Course.objects.filter(
        admin__in=[request.user, ]).order_by('created_at')
    return render(request, 'useraccount/courses.html', locals())


@csrf_exempt
@login_required
def course_detail(request, pk):
    if not request.user.is_staff:
        raise Http404
    course = Course.objects.get(admin=request.user, pk=pk)
    userscores = UserScore.objects.filter(course=course)
    if request.method == 'POST':
        f = request.FILES.get('file')
        wb = xlrd.open_workbook(
            filename=None, file_contents=f.read()
        )
        table = wb.sheets()[0]
        row = table.nrows
        error = []
        #['学号'，'期中成绩'， '期末成绩','平时成绩'，'实验成绩'，'补考成绩']
        for i in xrange(row):
            col = table.row_values(i)
            stuId = col[0]
            midterm = col[1] or 0
            final_exam = col[2] or 0
            usual = col[3] or 0
            experimental = col[4] or 0
            retest = col[5] or 0
            user = User.objects.get(stuId=col[0])
            userscore = UserScore.objects.filter(course=course, user=user)
            if userscore:
                userscore.update(midterm=midterm, final_exam=final_exam,
                                    usual=usual, experimental=experimental, retest=retest)
            else:
                UserScore.objects.create(course=course, user=user, midterm=midterm, final_exam=final_exam,
                                            usual=usual, experimental=experimental, retest=retest)
    if request.GET.get('download', False):
        title = [u'姓名', u'英文名', u'学号', '期中考试成绩', u'期末考试成绩',
                 u'平时成绩', u'实验成绩', u'补考成绩', u'总分', u'绩点']
        excel = []
        name = '{}.xsl'.format(course.name)
        teams = set(userscores.values_list('user__team__gradeId'))
        for team in teams:
            all_data = [title, ]
            retest = [title, ]
            good = [title, ]
            for userscore in userscores.filter(user__team__gradeId=team[0]):
                user = userscore.user
                data = [user.name, user.username, user.stuId, userscore.midterm or 0,
                             userscore.final_exam or 0, userscore.usual or 0, userscore.experimental or 0,
                             userscore.retest or 0, userscore.total_score, userscore.points]
                if userscore.total_score:
                    if userscore.total_score >= 85:
                        good.append(data)
                    elif userscore.total_score < 60:
                        retest.append(data)
                all_data.append(data)
            excel.append({'name': str(team[0]), 'data': all_data})
            excel.append({'name': '{}{}'.format(team[0], u'优秀学生'), 'data': good})
            excel.append({'name': '{}{}'.format(team[0], u'补考学生'), 'data': retest})
        response = HttpResponse(generate_xls_multisheet(
            excel), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = u'attachment; filename=%s' % urllib.quote(
            name.encode('utf8'))
        return response
    return render(request, 'useraccount/course_detail.html', locals())

@login_required
def user_lesson(request):
    user = request.user
    school_term = request.GET.get('school_term')
    school_terms = SchoolTerm.objects.all()
    if school_term:
        school_term = SchoolTerm.objects.get(name=school_term)
    else:
        school_term = SchoolTerm.now_schoolterm()
    userscore = UserScore.objects.filter(course__school_term=school_term, user=user)
    courses = [us.course for us in userscore]
    class_schedule = ClassSchedule.objects.filter(Q(course__admin__in=[user,])|Q(course__in=courses), course__school_term=school_term)
    schedule_dict = ClassSchedule.sort(class_schedule)
    return render(request, 'useraccount/lesson.html', locals())

@login_required
def course_analyze(request):
    user = request.user
    if not user.is_staff:
        raise Http404



