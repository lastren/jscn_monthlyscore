# -*- coding: utf-8 -*-

from django.conf.urls import include, url
import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.homeView, name='home'),

    url(r'^addTask$', views.addTask, name='addTask'),
    url(r'^editTask$', views.editTask, name='editTask'),

    url(r'^addReport$', views.addReport, name='addReport'),
    url(r'^editReport$', views.editReport, name='editReport'),

    url(r'^saveReport/([0-4]{1})/$', views.saveReport, name='saveReport'),


    url(r'^ajaxedittask$', views.ajaxedittask, name='ajaxedittask'),
    url(r'^ajaxdeletetask$', views.ajaxdeletetask, name='ajaxdeletetask'),

]