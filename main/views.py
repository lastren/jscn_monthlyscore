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
from django.views.generic import ListView

# Create your views here.
# Create your views here.
def homeView(request):
    template_name = 'home.html'

    account = request.session['account']
    if account is None:
        redirect(reverse('accounts:login'))

    newmonth = getNewMonth(account)

    if newmonth is None:
        newbtn=False
    else:
        newbtn=True
    return render(request, template_name,{'newbtn':newbtn})

def getNewMonth(account):
    newmonth = None

    user = User.objects.get(username=account)
    profile = user.profile
    currentDate = datetime.date.today()
    startDate = profile.startDate
    reports = profile.reports

    if reports.exists():
        latestreport = profile.reports.latest('month')
        latestmonth = latestreport.month
        mb1 = utils.utils.months_behind(latestmonth, startDate)
        if mb1 < 0:
            newmonth = startDate
        else:
            mb2 = utils.utils.months_behind(currentDate, latestmonth)
            if mb2 > 0:
                newmonth = utils.utils.datetime_offset_by_month(latestmonth, 1)
    else:
        newmonth = profile.startDate

    if newmonth is not None:
        # 把所有对有效日期都定为当月的1号
        newmonth = datetime.date(newmonth.year, newmonth.month, 1)
        return newmonth
    else:
        return None


def addReport(request):
    errResponse = redirect(reverse('main:home'))
    template_name = 'editReport.html'

    account = request.session['account']
    user = User.objects.get(username=account)
    profile = user.profile
    newmonth = getNewMonth(account)

    if newmonth is None:
        messages.error(request, '无法创建报告：月份参数缺失')
        return errResponse

    #在addreport页面刷新导致的问题，tobemended
    #elif utils.utils.months_behind(newmonth, latestmonth) == 0:

    report = Report()
    report.month=newmonth
    report.author=profile
    report.save()

    reportForm = forms.ReportForm()

    return render(request, template_name, {
        'reportForm': reportForm,
        'reportid':report.pk,
        'reportmonth':report.month
    })

def editReport(request,form):
    template_name = 'editReport.html'
    return render(request,template_name,{'form':form})

def saveReport(request,type):
    if request.method == 'POST':
        form = forms.ReportForm(request.POST)
        reportid = request.POST.get('reportid')
        if form.is_valid():
            report= get_object_or_404(Report,pk=int(reportid))
            report.scoreL1 = form.cleaned_data['scoreL']
            report.scoreS1 = form.cleaned_data['scoreS']
            report.scoreD1 = form.cleaned_data['scoreD']
            report.scoreR1 = form.cleaned_data['scoreR']
            if type ==0:
                report.status = report.STATUS[0]
            elif type ==1:
                report.status = report.STATUS[1]
            report.save()

    return redirect(reverse('main:home'))

# def getReports(request,type):
#     template_name = 'reportList.html'

class ReportList(ListView):
    model = Report
    template_name = 'reportList.html'
    context_object_name = 'report_list'

    def get_queryset(self):
        self.type = self.args[0]
        profile = self.request.user.profile
        reports = profile.reports.filter(status=self.type)
        return reports

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super(ReportList, self).get_context_data(**kwargs)
    #     # Add in the publisher
    #     if self.type == u'0':
    #         title = u'未提交的报告'
    #     elif self.type == u'1':
    #         title = u'未审核的报告'
    #     context['title'] = title
    #     return context



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




