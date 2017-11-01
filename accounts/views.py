# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
import datetime
import utils.utils

import forms,models
import logging
logger = logging.getLogger('aa')


def loginView(request):
    template_name = 'accounts/login.html'
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # 登陆成功，保存关键数据到session中
                    profile = models.Profile.objects.get(user=user)

                    request.session['userrole'] = profile.userRole
                    request.session['userdept'] = profile.department
                    request.session['username'] = profile.displayName
                    request.session['account'] = username

                    return redirect(reverse('main:home'))

            # Return an 'invalid login' error message.
            messages.error(request, '用户名或密码不正确，请核对后重新输入')
            return redirect(reverse('accounts:login'))
    else:
        form = forms.LoginForm()
        return render(request, template_name,{'form':form})


def logoutView(request):
    logout(request)
    return redirect(reverse('accounts:login'))



