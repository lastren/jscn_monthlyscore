# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
    MANAGER=u'manager'
    LEADER=u'leader'
    WORKER=u'worker'
    USER_ROLE = (
        (MANAGER, u'部门负责人'),
        (LEADER, u'科室负责人'),
        (WORKER, u'职员'),
    )

    DP1 = u'科室1'
    DP2 = u'科室2'
    DP3 = u'科室3'
    DEPARTMENT =(
        (DP1, u'科室1'),
        (DP2, u'科室2'),
        (DP3, u'科室3'),
    )

    displayName = models.CharField(verbose_name=u'用户名称',max_length=128,default=u'请输入用户名')
    user = models.OneToOneField(User,verbose_name=u'用户')
    userRole = models.CharField(
        max_length=20,
        choices=USER_ROLE,
        default=WORKER,
    )
    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT,
        default=DP1,
    )
    startDate = models.DateField(verbose_name=u'启用日期',auto_now_add=True,blank=True)

    def __str__(self):
        return self.displayName

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'
        ordering = ['id']

