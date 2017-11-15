# -*- coding:utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名',max_length=20)
    password = forms.CharField(label=u'密码',max_length=256, widget=forms.PasswordInput)


class ChangePwForm(forms.Form):
    old_password = forms.CharField(label=u'原密码', max_length=256, widget=forms.PasswordInput)
    new_password = forms.CharField(label=u'新密码', max_length=256, widget=forms.PasswordInput)