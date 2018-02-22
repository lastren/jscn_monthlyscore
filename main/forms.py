# -*- coding:utf-8 -*-

from django import forms
import models

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields=['desc','done']
        widgets={
            'desc':forms.Textarea,
            'done': forms.Textarea,
        }

class ReportForm(forms.Form):
    scoreL = forms.DecimalField(
        max_value=35,
        min_value=0,
        widget=forms.NumberInput(attrs={'style':'width:100px'}),
    )
    scoreS = forms.DecimalField(
        max_value=30,
        min_value=0,
        widget=forms.NumberInput(attrs={'style':'width:100px'}),
    )
    scoreD = forms.DecimalField(
        max_value=30,
        min_value=0,
        widget=forms.NumberInput(attrs={'style':'width:100px'}),
    )
    scoreR = forms.DecimalField(
        max_value=5,
        min_value=0,
        widget=forms.NumberInput(attrs={'style':'width:100px'}),
    )
    note = forms.CharField(
        max_length=2048,
        widget= forms.Textarea,
        required=False,
    )








