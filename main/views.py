# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,reverse
import forms
from models import Report,Task
from django.http import HttpResponseRedirect
import datetime
from django.contrib.auth.models import User
import accounts
from accounts.models import Profile
import utils.utils
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

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

def editReport(request,reportid):
    template_name = 'editReport.html'

    report = get_object_or_404(Report,pk=int(reportid))

    reportForm = None

    tasksL = report.tasks.filter(type=u'1')
    tasksS = report.tasks.filter(type=u'2')
    tasksD = report.tasks.filter(type=u'3')

    #account = request.session['account']
    profile = request.user.profile
    imauthor=False
    if profile.pk == report.author.pk:
        imauthor = True

    imleader=False
    if profile.userRole == Profile.LEADER:
        imleader=True

    immanager=False
    if profile.userRole == Profile.MANAGER:
        immanager=True

    taskEditable = False
    if report.status == Report.STATUS_INITIAL:
        if imauthor:
            reportForm = forms.ReportForm({
                'scoreL': report.scoreL1,
                'scoreS': report.scoreS1,
                'scoreD': report.scoreD1,
                'scoreR': report.scoreR1,
            })
            taskEditable=True
        else:
            whenErrorHappens(request, u'无操作权限')
    elif report.status == Report.STATUS_SUBMITTOLEADER:
        if imauthor:
            reportForm = {
                'scoreL': report.scoreL1,
                'scoreS': report.scoreS1,
                'scoreD': report.scoreD1,
                'scoreR': report.scoreR1
            }
            template_name = 'editReport10.html'
        elif imleader:
            report.status=Report.STATUS_LEADERCHECK
            report.save()

            reportForm = {
                'scoreL': report.scoreL2,
                'scoreS': report.scoreS2,
                'scoreD': report.scoreD2,
                'scoreR': report.scoreR2
            }

            template_name = 'editReport21.html'
            return render(request, template_name, {
                'reportForm': reportForm,
                'reportmonth': report.month,
                'reportid': reportid,
                'tasksL': tasksL,
                'tasksS': tasksS,
                'tasksD': tasksD,
                'taskEditable': taskEditable,
                'scorel1':report.scoreL1,
                'scores1': report.scoreS1,
                'scored1': report.scoreD1,
                'scorer1': report.scoreR1
            })
        else:
            whenErrorHappens(request, u'无操作权限')








    return render(request,template_name,{
        'reportForm':reportForm,
        'reportmonth': report.month,
        'reportid':reportid,
        'tasksL':tasksL,
        'tasksS':tasksS,
        'tasksD':tasksD,
        'taskEditable':taskEditable
    })

def whenErrorHappens(request,errStr):
    errResponse = redirect(reverse('main:home'))
    messages.error(request, errStr)
    return errResponse


def saveReport(request,type):
    if request.method == 'POST':
        form = forms.ReportForm(request.POST)
        reportid = request.POST.get('reportid')
        if form.is_valid():
            report= get_object_or_404(Report,pk=int(reportid))

            if report.status == Report.STATUS_INITIAL:
                report.scoreL1 = form.cleaned_data['scoreL']
                report.scoreS1 = form.cleaned_data['scoreS']
                report.scoreD1 = form.cleaned_data['scoreD']
                report.scoreR1 = form.cleaned_data['scoreR']
                if type == Report.STATUS_INITIAL or type == Report.STATUS_SUBMITTOLEADER:
                    report.status = type
                    report.save()

    return redirect(reverse('main:home'))

#only change status, not the content,used for 1-0,3-2
def retrieveReport(request):
    if request.method == 'POST':
        reportid = request.POST.get('reportid')

        report = get_object_or_404(Report,pk=int(reportid))
        status = report.status
        profile = request.user.profile
        author = report.author

        if profile.pk == author.pk:
            if status == Report.STATUS_SUBMITTOLEADER:
                report.status= Report.STATUS_INITIAL
                report.save()
        elif profile.userRole==Profile.LEADER and profile.department==author.department:
            if status == Report.STATUS_SUBMITTOMANAGER:
                report.status = Report.STATUS_LEADERCHECK
                report.save()
            elif status == Report.STATUS_LEADERCHECK:
                report.status = Report.STATUS_RETURNBYLEADER
                report.save()

    return redirect(reverse('main:home'))


# def withdrawReport(request,aa):
#     return redirect(reverse('main:home'))

# def getReports(request,type):
#     template_name = 'reportList.html'

# @login_required
class ReportList(ListView):
    model = Report
    template_name = 'reportList.html'
    context_object_name = 'report_list'

    def get_queryset(self):
        self.type = self.args[0]
        self.imauthor = self.kwargs['imauthor']
        profile = self.request.user.profile

        if self.imauthor == u'1':
            reports = profile.reports.filter(status=self.type)
            return reports
        else:
            if profile.userRole==Profile.LEADER:
                if self.type != Report.STATUS_INITIAL and self.type != Report.STATUS_ARCHIVED:
                    reports = Report.objects.filter(author__department=profile.department
                                                    ).filter(status=self.type)
                    return reports
                else:
                    return None
            elif profile.userRole==Profile.MANAGER:
                if self.type == Report.STATUS_SUBMITTOMANAGER or self.type == Report.STATUS_MANAGERCHECK or self.type == Report.STATUS_RETURNBYMANAGER :
                    reports = Report.objects.filter(author__department=profile.department
                                                    ).filter(status = self.type)
                    return reports
                else:
                    return None
            else:
                return None








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
    # this cookie kv will be deleted in the js
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
    #this cookie kv will be deleted in the js
    response.set_cookie('tasktype', tasktype)
    return response




