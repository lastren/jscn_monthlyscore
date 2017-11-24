# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import accounts.models as acModels
from decimal import *

# Create your models here.
class Report(models.Model):
    STATUS_INITIAL = u'0'
    STATUS_SUBMITTOLEADER = u'1'
    STATUS_LEADERCHECK = u'2'
    STATUS_SUBMITTOMANAGER = u'3'
    STATUS_MANAGERCHECK = u'4'
    STATUS_ARCHIVED = u'5'
    STATUS_RETURNBYLEADER = u'6'
    STATUS_RETURNBYMANAGER = u'7'

    STATUS=(
        (STATUS_INITIAL, u'未提交'),
        (STATUS_SUBMITTOLEADER, u'已提交科室'),
        (STATUS_LEADERCHECK, u'科室审核中'),
        (STATUS_SUBMITTOMANAGER, u'已提交部门'),
        (STATUS_MANAGERCHECK, u'部门审核中'),
        (STATUS_ARCHIVED, u'已存档'),
        (STATUS_RETURNBYLEADER, u'退回员工'),
        (STATUS_RETURNBYMANAGER, u'退回科室'),
    )
    month=models.DateField(verbose_name=u'报告期号', db_index=True)
    status=models.CharField(
        choices=STATUS,
        default= u'0',
        max_length=10,
    )
    author=models.ForeignKey(acModels.Profile,related_name='reports')

    #scoreL1 = models.IntegerField(verbose_name=u'长期项目自评分', default=0)
    scoreL2 = models.DecimalField(verbose_name=u'长期项目科评分', default=0,max_digits=3,decimal_places=1)
    scoreL3 = models.DecimalField(verbose_name=u'长期项目部评分', default=0,max_digits=3,decimal_places=1)

    #scoreS1 = models.IntegerField(verbose_name=u'短期项目自评分', default=0)
    scoreS2 = models.DecimalField(verbose_name=u'短期项目科评分', default=0,max_digits=3,decimal_places=1)
    scoreS3 = models.DecimalField(verbose_name=u'短期项目部评分', default=0,max_digits=3,decimal_places=1)

    #scoreD1 = models.IntegerField(verbose_name=u'日常项目自评分', default=0)
    scoreD2 = models.DecimalField(verbose_name=u'日常项目科评分', default=0,max_digits=3,decimal_places=1)
    scoreD3 = models.DecimalField(verbose_name=u'日常项目部评分', default=0,max_digits=3,decimal_places=1)

    #scoreR1 = models.IntegerField(verbose_name=u'行为规范自评分', default=0)
    scoreR2 = models.DecimalField(verbose_name=u'行为规范科评分', default=0,max_digits=3,decimal_places=1)
    scoreR3 = models.DecimalField(verbose_name=u'行为规范部评分', default=0,max_digits=3,decimal_places=1)

    note1 = models.CharField(verbose_name=u'加分事由',max_length=2048,default=u'')
    note2 = models.CharField(verbose_name=u'科室批复', max_length=2048, default=u'')
    note3 = models.CharField(verbose_name=u'部门批复', max_length=2048, default=u'')

    # def getSum1(self):
    #     return self.scoreL1+self.scoreS1+self.scoreD1+self.scoreR1

    def getSum2(self):
        return self.scoreL2+self.scoreS2+self.scoreD2+self.scoreR2

    def getSum3(self):
        return self.scoreL3+self.scoreS3+self.scoreD3+self.scoreR3

    def getSumAll(self):
        return self.getSum2() * Decimal.from_float(0.5)+self.getSum3()*Decimal.from_float(0.5)


class Task(models.Model):
    desc=models.CharField(verbose_name=u'任务描述',max_length=2048,default=u'任务描述')
    done=models.CharField(verbose_name=u'完成内容',max_length=2048,default=u'完成内容')

    # startDate = models.DateField(verbose_name=u'起始日期', db_index=True,blank=True,null=True)
    # endDate = models.DateField(verbose_name=u'预计完成日期', db_index=True,blank=True,null=True)
    #
    # scoreByMe=models.IntegerField(verbose_name=u'自评分', default=0,blank=False)
    # scoreByLeader = models.IntegerField(verbose_name=u'科室评分', default=0)
    # scoreByManager = models.IntegerField(verbose_name=u'部门评分', default=0)

    report= models.ForeignKey(Report,
                              on_delete=models.CASCADE,
                              related_name='tasks',)

    TYPE=(
        (u'1', u'长期项目'),
        (u'2', u'短期项目'),
        (u'3', u'日常运维'),
    )

    type=models.CharField(
        choices=TYPE,
        default=u'1',
        max_length=10,
    )

    class Meta:
        verbose_name = u'任务信息'
        ordering = ['id']



