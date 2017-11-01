# -*- coding:utf-8 -*-

from django import forms
import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields=['desc','done']
        widgets={
            'desc':forms.Textarea(attrs={
                'rows':2,
                'cols':40
            }),
            'done': forms.Textarea(attrs={
                'rows': 2,
                'cols': 40
            }),
        }

class ReportForm(forms.Form):
    scoreL = forms.IntegerField(
        max_value=35,
        min_value=0,
    )
    scoreS = forms.IntegerField(
        max_value=30,
        min_value=0,
    )
    scoreD = forms.IntegerField(
        max_value=30,
        min_value=0,
    )
    scoreR = forms.IntegerField(
        max_value=5,
        min_value=0,
    )







