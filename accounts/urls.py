# -*- coding: utf-8 -*-

from django.conf.urls import include, url
import views

app_name = 'accounts'
urlpatterns = [
    url(r'^login/$', views.loginView, name='login'),
    url(r'^logout/$', views.logoutView, name='logout'),
    #url(r'^profile/$', views.profileView, name='profile'),
]
