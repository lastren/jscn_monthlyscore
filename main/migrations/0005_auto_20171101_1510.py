# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20171101_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('0', '\u672a\u63d0\u4ea4'), ('1', '\u5f851\u5ba1'), ('2', '\u5f852\u5ba1'), ('3', '\u5b8c\u6210')], default='0', max_length=10),
        ),
    ]
