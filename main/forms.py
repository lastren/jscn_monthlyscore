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

class ReportForm(forms.ModelForm):
    class Meta:
        model= models.Report
        fields=['scoreL1','scoreS1','scoreD1','scoreR1']





