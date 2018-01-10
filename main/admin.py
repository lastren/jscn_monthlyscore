# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Report

# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id','status','month','author',)
    search_fields = ('author',)
    list_filter = ['author']


admin.site.register(Report,ReportAdmin)