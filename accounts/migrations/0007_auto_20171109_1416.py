# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20171109_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='department',
            field=models.CharField(choices=[('0', '\u65e0'), ('1', '\u79d1\u5ba41'), ('2', '\u79d1\u5ba42'), ('3', '\u79d1\u5ba43')], default='0', max_length=20),
        ),
    ]
