# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20171113_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='desc',
            field=models.CharField(default='\u4efb\u52a1\u63cf\u8ff0', max_length=2048, verbose_name='\u4efb\u52a1\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='task',
            name='done',
            field=models.CharField(default='\u5b8c\u6210\u5185\u5bb9', max_length=2048, verbose_name='\u5b8c\u6210\u5185\u5bb9'),
        ),
    ]