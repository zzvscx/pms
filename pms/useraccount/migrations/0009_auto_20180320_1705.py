# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-20 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0008_auto_20180320_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='campus',
            field=models.IntegerField(choices=[(0, '\u6e2d\u6c34\u6821\u533a'), (1, '\u672c\u90e8'), (2, '\u5c0f\u5be8\u6821\u533a'), (3, '\u96c1\u5854\u6821\u533a')], default=0, verbose_name='\u6240\u5c5e\u6821\u533a'),
        ),
        migrations.AlterField(
            model_name='user',
            name='desc',
            field=models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8'),
        ),
    ]
