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
from models import Profile
from django.contrib.auth.decorators import login_required

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
                    request.session['userdept'] = profile.get_department_display()
                    request.session['username'] = profile.displayName
                    request.session['account'] = username
                    request.session['depts'] = {Profile.DP1:Profile.DP1NAME,
                                                Profile.DP2: Profile.DP2NAME,
                                                Profile.DP3: Profile.DP3NAME
                                                }
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


@login_required
def changePwView(request):
    if request.method == 'POST':
        cpf = forms.ChangePwForm(request.POST)
        if cpf.is_valid():
            username = request.session['account']
            old_password = cpf.cleaned_data['old_password']
            new_password = cpf.cleaned_data['new_password']
            print(old_password)
            print(new_password)
            ##判断用户原密码是否匹配
            user = authenticate(username=request.user.username, password=old_password)
            if user is not None and user.is_active:
                user.set_password(new_password)
                user.save()

                info = '密码修改成功,请重新登录!'
                messages.info(request, info)
                return redirect(reverse('accounts:login'))
            else:
                info = '密码不正确，请重新输入!'
                messages.info(request, info)
                return redirect(reverse('accounts:changepw'))

    else:
        cpf = forms.ChangePwForm()
        return render(request, 'accounts/changepw.html',{'form':cpf})

