#-*- coding: utf-8 -*-

from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from useraccount.models import User,UserScore
from course.models import Academy, Department, Grade, Category,\
                    SchoolTerm,Schedule,Course


def sendmail(title, content, to, files=None, from_email='default', cc=None, ):
    if isinstance(to, list):
        to_addr = to
        to = ",".join(to)
    else:
        to_addr = [to]
    cc = cc or []
    host_config = getattr(settings, 'EMAIL_HOST_CONFIG').get(from_email)
    smtp = smtplib.SMTP()
    smtp.connect(getattr(settings, 'EMAIL_HOST'), getattr(settings, 'EMAIL_PORT'))
    EMAIL_HOST_USER = host_config.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = host_config.get('EMAIL_HOST_PASSWORD')
    from_email = host_config.get('DEFAULT_FROM_EMAIL')
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = from_email or getattr(settings, 'DEFAULT_FROM_EMAIL')
    msg['To'] = to
    msg['Cc'] = ",".join(cc or [])
    msg['Subject'] = title
    msg.attach(MIMEText(content, 'html', 'utf8'))
    for x in files or []:
        if isinstance(x, basestring):
            with open(x) as f:
                msg.attach(MIMEApplication(
                    f.read(),
                    Content_Disposition='attachment; filename="%s"' % os.path.basename(x).encode('utf8'),
                    Name=os.path.basename(x).encode('utf8')
                ))
        else:
            name, content, _ = x
            msg.attach(MIMEApplication(
                content,
                Content_Disposition='attachment; filename="%s"' % name.encode('utf8'),
                Name=name.encode('utf8')
            ))

    res = smtp.sendmail(from_email or getattr(settings, 'DEFAULT_FROM_EMAIL'), to_addr + cc, msg.as_string())
    smtp.quit()
    return res

def add():
    academy = Academy.objects.create(name=u'信息学院')
    department = Department.objects.create(name=u'电子信息工程', academy=academy)
    grade = Grade.objects.create(name=u'电子信息工程二班', gradeId='2014240302', department=department)
    User.objects.create(username='zhangsongwei', password='zxcasdqwe'name=u'张松伟', sex=u'男', stuId='201424030220',term=grade,intake='2014-09-01',leave='2018-09-01',term='2014')
    teacher = User.objects.create(username='teacher',password='zxcasdqwe')
    category = Category.objects.create(name=u'公共基础课')
    SchoolTerm.add_schoolterm()
    Schedule.add_schedule()
    Course.objects.create(name=u'高数上', code=1, numbering=1,category=category,admin=[teacher,],
        schoolterm=SchoolTerm.objects.get(name=''))

    