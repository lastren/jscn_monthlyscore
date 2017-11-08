# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-28 09:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(db_index=True, verbose_name='\u62a5\u544a\u671f\u53f7')),
                ('status', models.CharField(choices=[('1', '\u672a\u63d0\u4ea4'), ('2', '\u5f851\u5ba1'), ('3', '\u5f852\u5ba1'), ('4', '\u5b8c\u6210')], default='1', max_length=10)),
                ('scoreL1', models.IntegerField(default=0, verbose_name='\u957f\u671f\u9879\u76ee\u81ea\u8bc4\u5206')),
                ('scoreL2', models.IntegerField(default=0, verbose_name='\u957f\u671f\u9879\u76ee\u79d1\u8bc4\u5206')),
                ('scoreL3', models.IntegerField(default=0, verbose_name='\u957f\u671f\u9879\u76ee\u90e8\u8bc4\u5206')),
                ('scoreS1', models.IntegerField(default=0, verbose_name='\u77ed\u671f\u9879\u76ee\u81ea\u8bc4\u5206')),
                ('scoreS2', models.IntegerField(default=0, verbose_name='\u77ed\u671f\u9879\u76ee\u79d1\u8bc4\u5206')),
                ('scoreS3', models.IntegerField(default=0, verbose_name='\u77ed\u671f\u9879\u76ee\u90e8\u8bc4\u5206')),
                ('scoreD1', models.IntegerField(default=0, verbose_name='\u65e5\u5e38\u9879\u76ee\u81ea\u8bc4\u5206')),
                ('scoreD2', models.IntegerField(default=0, verbose_name='\u65e5\u5e38\u9879\u76ee\u79d1\u8bc4\u5206')),
                ('scoreD3', models.IntegerField(default=0, verbose_name='\u65e5\u5e38\u9879\u76ee\u90e8\u8bc4\u5206')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(default='\u4efb\u52a1\u63cf\u8ff0', max_length=512, verbose_name='\u4efb\u52a1\u63cf\u8ff0')),
                ('done', models.CharField(default='\u5b8c\u6210\u5185\u5bb9', max_length=512, verbose_name='\u5b8c\u6210\u5185\u5bb9')),
                ('type', models.CharField(choices=[('1', '\u957f\u671f\u9879\u76ee'), ('2', '\u77ed\u671f\u9879\u76ee'), ('3', '\u65e5\u5e38\u8fd0\u7ef4')], default='1', max_length=10)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='main.Report')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u4efb\u52a1\u4fe1\u606f',
            },
        ),
    ]