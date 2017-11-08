# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 09:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayName', models.CharField(default='\u8bf7\u8f93\u5165\u7528\u6237\u540d', max_length=128, verbose_name='\u7528\u6237\u540d\u79f0')),
                ('userRole', models.CharField(choices=[('manager', '\u90e8\u95e8\u8d1f\u8d23\u4eba'), ('leader', '\u79d1\u5ba4\u8d1f\u8d23\u4eba'), ('worker', '\u804c\u5458')], default='worker', max_length=20)),
                ('department', models.CharField(choices=[('\u79d1\u5ba41', '\u79d1\u5ba41'), ('\u79d1\u5ba42', '\u79d1\u5ba42'), ('\u79d1\u5ba43', '\u79d1\u5ba43')], default='\u79d1\u5ba41', max_length=20)),
                ('startDate', models.DateField(auto_now_add=True, verbose_name='\u542f\u7528\u65e5\u671f')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u7528\u6237\u4fe1\u606f',
            },
        ),
    ]