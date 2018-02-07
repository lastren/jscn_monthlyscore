# -*- coding: utf-8 -*-

from django.conf.urls import include, url
import views
from main.views import ReportList

app_name = 'main'
urlpatterns = [
    url(r'^$', views.homeView, name='home'),
    url(r'^history$', views.historyView, name='history'),

    url(r'^addReport$', views.addReport, name='addReport'),
    url(r'^editReport/([0-9]+)/$', views.editReport, name='editReport'),

    url(r'^saveReport/([0-9]{1})/$', views.saveReport, name='saveReport'),
    url(r'^retrieveReport$', views.retrieveReport, name='retrieveReport'),

    # url(r'^getReports/([0-4]{1})/$', views.saveReport, name='getReports'),
    url(r'^getMyReports/([0-9]{1,2})/$', ReportList.as_view(),{'imauthor':u'1'},name='getMyReports'),
    url(r'^getTheirReports/([0-9]{1})/$', ReportList.as_view(),{'imauthor':u'0'},name='getTheirReports'),
    url(r'^getDeptReports/([0-9]{1})/([1-9]{1})/$', ReportList.as_view(),name='getDeptReports'),
    #leader get other department's reports
    url(r'^getExtraReports/([0-9]{1})/([1-9]{1})/$', views.getExtraReports,name='getExtraReports'),
    url(r'^editExtraReport/([0-9]+)/$', views.editExtraReport, name='editExtraReport'),

    url(r'^ajaxedittask$', views.ajaxedittask, name='ajaxedittask'),
    url(r'^ajaxdeletetask$', views.ajaxdeletetask, name='ajaxdeletetask'),
    url(r'^ajaxgetreports$', views.ajaxgetreports, name='ajaxgetreports'),

    url(r'^toexcel$', views.toexcel, name='toexcel'),

]