# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-03 07:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_course_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.CharField(blank=True, max_length=32, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='schedule',
        ),
        migrations.AddField(
            model_name='classschedule',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
        migrations.AddField(
            model_name='classschedule',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Schedule'),
        ),
    ]
