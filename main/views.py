# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,reverse
import forms
from models import Report,Task
from django.http import HttpResponseRedirect
import datetime
from django.contrib.auth.models import User
import accounts
import utils.utils
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.
# Create your views here.
def homeView(request):
    template_name = 'home.html'

    username = request.session['username']
    newmonth = getNewMonth(username)

    if newmonth is None:
        newbtn=False
    else:
        newbtn=True
    return render(request, template_name,{'newbtn':newbtn})

def getNewMonth(username):
    newmonth = None

    userid = User.objects.get(username=username)
    profile = accounts.models.Profile.objects.get(user_id=userid)
    currentDate = datetime.date.today()
    startDate = profile.startDate
    reports = profile.reports
    if reports.count() == 0:
        newmonth = profile.startDate
    else:
        latestreport = profile.reports.latest('month')
        latestmonth = latestreport.month
        mb1 = utils.utils.months_behind(latestmonth, startDate)
        if mb1 < 0:
            newmonth = startDate
        else:
            mb2 = utils.utils.months_behind(currentDate, latestmonth)
            if mb2 > 0:
                newmonth = utils.utils.datetime_offset_by_month(latestmonth, 1)

    if newmonth is not None:
        # 把所有对有效日期都定为当月的1号
        newmonth = datetime.date(newmonth.year, newmonth.month, 1)

    return newmonth


def addReport(request):
    errResponse = redirect(reverse('main:home'))
    template_name = 'editReport.html'

    username = request.session['username']
    userid = User.objects.get(username=username)
    profile = accounts.models.Profile.objects.get(user_id=userid)
    newmonth = getNewMonth(username)

    if newmonth is None:
        messages.error(request, '无法创建报告：月份参数缺失')
        return errResponse

    #在addreport页面刷新导致的问题，tobemended
    #elif utils.utils.months_behind(newmonth, latestmonth) == 0:

    report = Report()
    report.month=newmonth
    report.author=profile
    report.save()

    reportForm = forms.ReportForm(instance=report)

    return render(request, template_name, {
        'reportForm': reportForm,
        'reportid':report.pk,
        'reportmonth':report.month
    })

def editReport(request,form):
    template_name = 'editReport.html'
    return render(request,template_name,{'form':form})

def addTask(request):
    template_name = 'editTask.html'
    return render(request,template_name)

def editTask(request):
    template_name = 'editTask.html'
    form = forms.TaskForm()
    if request.method == 'POST':
        reportid = request.POST['reportid']
        taskid = request.POST['taskid']
        taskdesc = request.POST['desc']
        taskdone = request.POST['done']

        if reportid == "":
            report = Report()
            report.month = datetime.datetime.strptime(request.POST['month'],"%Y-%m")
            print(report.month)
            report.save()
        else:
            report = Report.objects.get(pk=reportid)

        if taskid == "":
            task = Task()
        else:
            task = Task.objects.get(pk=taskid)

        task.desc=taskdesc
        task.done=taskdone
        task.report=report
        task.save()

        form=forms.ReportForm(report)
        return HttpResponseRedirect(reverse('main:editReport',args=(form,)))
    else:
        pass

    return render(request,template_name,{'form':form})


def ajaxedittask(request):
    reportid = request.POST['reportid']
    taskid = request.POST['taskid']
    taskdesc = request.POST['taskdesc']
    taskdone = request.POST['taskdone']
    tasktype = request.POST['tasktype']

    if reportid=="":
        messages.error(request, '编辑报告出错，请重新登录')
        return redirect(reverse('main:home'))

    #report = Report.objects.get(pk=int(reportid))
    report = get_object_or_404(Report,pk=int(reportid))

    if taskid=="":
        task = Task()
        task.type = tasktype
    else:
        #task = Task.objects.get(pk=int(taskid))
        task = get_object_or_404(Task,pk=int(taskid))

    task.desc = taskdesc
    task.done = taskdone
    task.report = report
    task.save()

    tasks = report.tasks.filter(type=tasktype)
    template_name = 'tasks.html'
    # request.session['reportid'] = report.pk
    response = render(request,template_name,{'tasks':tasks})
    response.set_cookie('tasktype',tasktype)
    return response


def ajaxdeletetask(request):
    template_name = 'tasks.html'

    taskid = request.POST['taskid']
    #task = Task.objects.get(pk=int(taskid))
    task = get_object_or_404(Task, pk=int(taskid))

    tasktype = task.type
    report = task.report
    task.delete()

    tasks = report.tasks.filter(type=tasktype)

    response = render(request, template_name, {'tasks': tasks})
    response.set_cookie('tasktype', tasktype)
    return response




