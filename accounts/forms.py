# -*- coding:utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label=u'用户名',max_length=20)
    password = forms.CharField(label=u'密码',max_length=256, widget=forms.PasswordInput)


class ChangePwForm(forms.Form):
    old_password = forms.CharField(label=u'原密码', max_length=256, widget=forms.PasswordInput)
    new_password = forms.CharField(label=u'新密码', max_length=256, widget=forms.PasswordInput)
    new_password_1 = forms.CharField(label=u'重复新密码', max_length=256, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ChangePwForm, self).clean()
        np = cleaned_data.get('new_password')
        np1 = cleaned_data.get('new_password_1')

        if np != np1:
            raise forms.ValidationError(
                u'两次密码输入不一致，请重新输入'
            )

        # return cleaned_data