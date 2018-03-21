# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-21 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20180321_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolterm',
            name='term',
        ),
        migrations.RemoveField(
            model_name='schoolterm',
            name='year',
        ),
        migrations.AddField(
            model_name='schoolterm',
            name='name',
            field=models.CharField(default=1, max_length=32, verbose_name='\u5b66\u5e74\u5b66\u671f'),
            preserve_default=False,
        ),
    ]
