# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,reverse
import forms
from models import Report,Task,ExtraReport
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
from django.utils.decorators import method_decorator
import xlwt
from utils import FitSheetWrapper
from django.http import HttpResponse
from decimal import *

# Create your views here.
# Create your views here.
@login_required
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


@login_required
def addReport(request):
    errResponse = redirect(reverse('main:home'))
    template_name = 'editReportwe.html'

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

    for department in [u'1', u'2', u'3']:
        if request.user.profile.department == department:
            pass
        else:
            x = ExtraReport(leader=department)
            x.report = report
            x.save()

    #reportForm = forms.ReportForm()

    reportForm = {
        'note': report.note1,
    }

    return render(request, template_name, {
        'reportForm': reportForm,
        'reportid':report.pk,
        'reportmonth':report.month,
    })

@login_required
def editReport(request,reportid):
    report = get_object_or_404(Report,pk=int(reportid))

    reportForm = None

    tasksL = report.tasks.filter(type=u'1')
    tasksS = report.tasks.filter(type=u'2')
    tasksD = report.tasks.filter(type=u'3')

    context={
                'reportmonth': report.month,
                'reportid': reportid,
                'tasksL': tasksL,
                'tasksS': tasksS,
                'tasksD': tasksD
            }

    imauthor,imleader,immanager = checkMyRole(request.user.profile,report.author)

    if report.status == Report.STATUS_INITIAL:
        if imauthor:
            # reportForm = forms.ReportForm({
            #     'scoreL': report.scoreL1,
            #     'scoreS': report.scoreS1,
            #     'scoreD': report.scoreD1,
            #     'scoreR': report.scoreR1,
            # })
            reportForm = {
                'note': report.note1,
            }
            context['reportForm']=reportForm
            context['note2']=report.note2
            context['note3'] = report.note3
            return render(request, 'editReportwe.html', context)
        else:
            whenErrorHappens(request, u'无操作权限')
    elif report.status in [Report.STATUS_SUBMITTOLEADER, Report.STATUS_LEADERCHECK]:
        if imauthor:
            # reportForm = {
            #     'scoreL': report.scoreL1,
            #     'scoreS': report.scoreS1,
            #     'scoreD': report.scoreD1,
            #     'scoreR': report.scoreR1,
            # }
            # context['reportForm'] = reportForm
            context['note1'] = report.note1
            context['hasbtn']= report.status == Report.STATUS_SUBMITTOLEADER
            return render(request, 'editReportwr.html', context)
        elif imleader:
            report.status=Report.STATUS_LEADERCHECK
            report.save()

            reportForm = forms.ReportForm({
                'scoreL': report.scoreL2,
                'scoreS': report.scoreS2,
                'scoreD': report.scoreD2,
                'scoreR': report.scoreR2,
                'note':report.note2,
            })
            context['reportForm'] = reportForm
            # context['scorel1']=report.scoreL1
            # context['scores1'] = report.scoreS1
            # context['scored1'] = report.scoreD1
            # context['scorer1'] = report.scoreR1

            context['note1'] = report.note1
            context['note3'] = report.note3

            context['author'] = report.author
            return render(request, 'editReportle.html',context)
        else:
            whenErrorHappens(request, u'无操作权限')
    elif report.status == Report.STATUS_RETURNBYLEADER:
        if imauthor:
            # reportForm = forms.ReportForm({
            #     'scoreL': report.scoreL1,
            #     'scoreS': report.scoreS1,
            #     'scoreD': report.scoreD1,
            #     'scoreR': report.scoreR1,
            # })
            reportForm = {
                'note': report.note1,
            }
            context['reportForm'] = reportForm
            context['note2']=report.note2
            context['note3'] = report.note3

            return render(request, 'editReportwe.html', context)
        elif imleader:
            # context['scorel1'] = report.scoreL1
            # context['scores1'] = report.scoreS1
            # context['scored1'] = report.scoreD1
            # context['scorer1'] = report.scoreR1
            context['scorel2'] = report.scoreL2
            context['scores2'] = report.scoreS2
            context['scored2'] = report.scoreD2
            context['scorer2'] = report.scoreR2
            context['hasbtn'] = False
            context['author'] = report.author

            context['note1'] = report.note1
            context['note2'] = report.note2
            context['note3'] = report.note3
            context['shownote'] = True

            return render(request, 'editReportlr.html', context)
        else:
            whenErrorHappens(request, u'无操作权限')
    elif report.status in [Report.STATUS_SUBMITTOMANAGER_DONE, Report.STATUS_SUBMITTOMANAGER_WAIT, Report.STATUS_MANAGERCHECK]:
        if imauthor:
            # reportForm = {
            #     'scoreL': report.scoreL1,
            #     'scoreS': report.scoreS1,
            #     'scoreD': report.scoreD1,
            #     'scoreR': report.scoreR1,
            # }
            # context['reportForm'] = reportForm
            context['note1'] = report.note1
            context['hasbtn'] = False
            return render(request, 'editReportwr.html', context)
        elif imleader:
            # context['scorel1'] = report.scoreL1
            # context['scores1'] = report.scoreS1
            # context['scored1'] = report.scoreD1
            # context['scorer1'] = report.scoreR1
            context['scorel2'] = report.scoreL2
            context['scores2'] = report.scoreS2
            context['scored2'] = report.scoreD2
            context['scorer2'] = report.scoreR2
            context['hasbtn'] = report.status in [Report.STATUS_SUBMITTOMANAGER_WAIT, Report.STATUS_SUBMITTOMANAGER_DONE]
            context['author'] = report.author

            context['note1'] = report.note1
            context['note2'] = report.note2
            context['shownote'] = False

            return render(request, 'editReportlr.html', context)
        elif immanager:
            report.status = Report.STATUS_MANAGERCHECK
            report.save()
            extraReports = report.extraReports.all()
            for xr in extraReports:
                if xr.status == ExtraReport.STATUS_SUBMITTOMANAGER:
                    xr.status = ExtraReport.STATUS_MANAGERCHECK
                    xr.save()

            reportForm = forms.ReportForm({
                'scoreL': report.scoreL3,
                'scoreS': report.scoreS3,
                'scoreD': report.scoreD3,
                'scoreR': report.scoreR3,
                'note': report.note3,
            })
            context['reportForm'] = reportForm

            # context['scorel2'] = report.scoreL2
            # context['scores2'] = report.scoreS2
            # context['scored2'] = report.scoreD2
            # context['scorer2'] = report.scoreR2
            s1 = (report.author.department, [report.scoreL2, report.scoreS2, report.scoreD2, report.scoreR2])
            extraReports = report.extraReports.all()
            if extraReports.count() == 2:
                s2 = (extraReports[0].leader,
                      [extraReports[0].scoreL, extraReports[0].scoreS, extraReports[0].scoreD, extraReports[0].scoreR])
                s3 = (extraReports[1].leader,
                      [extraReports[1].scoreL, extraReports[1].scoreS, extraReports[1].scoreD, extraReports[1].scoreR])
                s = (s1, s2, s3)
                ss = sorted(s, key=lambda x: x[0])
                context['dept1Score'] = ss[0][1]
                context['dept2Score'] = ss[1][1]
                context['dept3Score'] = ss[2][1]
                deptSum = getDeptSum(report.getSum2(),extraReports[0].getSum(),extraReports[1].getSum())
                context['deptsum'] = deptSum
            else:
                if s1[0] == u'1':
                    context['dept1Score'] = s1[1]
                    context['dept2Score'] = ['-', '-', '-', '-']
                    context['dept3Score'] = ['-', '-', '-', '-']
                elif s1[0] == u'2':
                    context['dept1Score'] = ['-', '-', '-', '-']
                    context['dept2Score'] = s1[1]
                    context['dept3Score'] = ['-', '-', '-', '-']
                else:
                    context['dept1Score'] = ['-', '-', '-', '-']
                    context['dept2Score'] = ['-', '-', '-', '-']
                    context['dept3Score'] = s1[1]

                context['deptsum'] = report.getSum2()

            context['author'] = report.author
            context['department'] = report.author.get_department_display()

            context['note1'] = report.note1
            context['note2'] = report.note2

            return render(request, 'editReportme.html', context)
        else:
            whenErrorHappens(request, u'无操作权限')
    elif report.status == Report.STATUS_RETURNBYMANAGER:
        if imauthor:
            # reportForm = {
            #     'scoreL': report.scoreL1,
            #     'scoreS': report.scoreS1,
            #     'scoreD': report.scoreD1,
            #     'scoreR': report.scoreR1,
            # }
            # context['reportForm'] = reportForm
            context['note1'] = report.note1
            context['hasbtn'] = False
            return render(request, 'editReportwr.html', context)
        if imleader:
            reportForm = forms.ReportForm({
                'scoreL': report.scoreL2,
                'scoreS': report.scoreS2,
                'scoreD': report.scoreD2,
                'scoreR': report.scoreR2,
                'note':report.note2,
            })
            context['reportForm'] = reportForm
            # context['scorel1'] = report.scoreL1
            # context['scores1'] = report.scoreS1
            # context['scored1'] = report.scoreD1
            # context['scorer1'] = report.scoreR1

            context['note1'] = report.note1
            context['note3'] = report.note3

            context['author'] = report.author
            return render(request, 'editReportle.html', context)
        if immanager:
            s1 = (report.author.department, [report.scoreL2,report.scoreS2,report.scoreD2,report.scoreR2])
            extraReports = report.extraReports.all()
            if extraReports.count() == 2:
                s2 = (extraReports[0].leader, [extraReports[0].scoreL,extraReports[0].scoreS,extraReports[0].scoreD,extraReports[0].scoreR])
                s3 = (extraReports[1].leader, [extraReports[1].scoreL,extraReports[1].scoreS,extraReports[1].scoreD,extraReports[1].scoreR])
                s = (s1, s2, s3)
                ss = sorted(s, key=lambda x: x[0])
                context['dept1Score'] = ss[0][1]
                context['dept2Score'] = ss[1][1]
                context['dept3Score'] = ss[2][1]
            else:
                if s1[0] == u'1':
                    context['dept1Score'] = s1[1]
                    context['dept2Score'] = ['-', '-', '-', '-']
                    context['dept3Score'] = ['-', '-', '-', '-']
                elif s1[0] == u'2':
                    context['dept1Score'] = ['-', '-', '-', '-']
                    context['dept2Score'] = s1[1]
                    context['dept3Score'] = ['-', '-', '-', '-']
                else:
                    context['dept1Score'] = ['-', '-', '-', '-']
                    context['dept2Score'] = ['-', '-', '-', '-']
                    context['dept3Score'] = s1[1]
            # context['scorel2'] = report.scoreL2
            # context['scores2'] = report.scoreS2
            # context['scored2'] = report.scoreD2
            # context['scorer2'] = report.scoreR2
            context['author'] = report.author
            context['department'] = report.author.get_department_display()

            context['note1'] = report.note1
            context['note2'] = report.note2
            context['note3'] = report.note3

            return render(request, 'editReportmr.html', context)
    elif report.status == Report.STATUS_ARCHIVED:
        s1 = (report.author.department, [report.scoreL2, report.scoreS2, report.scoreD2, report.scoreR2])
        extraReports = report.extraReports.all()
        if extraReports.count() == 2:
            s2 = (extraReports[0].leader,
                  [extraReports[0].scoreL, extraReports[0].scoreS, extraReports[0].scoreD, extraReports[0].scoreR])
            s3 = (extraReports[1].leader,
                  [extraReports[1].scoreL, extraReports[1].scoreS, extraReports[1].scoreD, extraReports[1].scoreR])
            s = (s1, s2, s3)
            ss = sorted(s, key=lambda x: x[0])
            context['dept1Score'] = ss[0][1]
            context['dept2Score'] = ss[1][1]
            context['dept3Score'] = ss[2][1]
            deptSum = getDeptSum(report.getSum2(), extraReports[0].getSum(), extraReports[1].getSum())
            context['sum'] = getTotalSum(deptSum,report.getSum3())
        else:
            if s1[0] == u'1':
                context['dept1Score'] = s1[1]
                context['dept2Score'] = ['-', '-', '-', '-']
                context['dept3Score'] = ['-', '-', '-', '-']
            elif s1[0] == u'2':
                context['dept1Score'] = ['-', '-', '-', '-']
                context['dept2Score'] = s1[1]
                context['dept3Score'] = ['-', '-', '-', '-']
            else:
                context['dept1Score'] = ['-', '-', '-', '-']
                context['dept2Score'] = ['-', '-', '-', '-']
                context['dept3Score'] = s1[1]

            context['sum'] = report.getSumAll()

        context['scorel3'] = report.scoreL3
        context['scores3'] = report.scoreS3
        context['scored3'] = report.scoreD3
        context['scorer3'] = report.scoreR3
        context['author'] = report.author
        context['department'] = report.author.get_department_display()

        context['note1'] = report.note1
        context['note2'] = report.note2
        context['note3'] = report.note3

        return render(request, 'editReporth.html', context)

    return redirect(reverse('main:home'))





def checkMyRole(profile,author):
    imauthor = False
    if profile.pk == author.pk:
        imauthor = True

    imleader = False
    if profile.userRole == Profile.LEADER:
        if profile.department == author.department:
            imleader = True

    immanager = False
    if profile.userRole == Profile.MANAGER:
        immanager = True

    return imauthor,imleader,immanager




def whenErrorHappens(request,errStr):
    errResponse = redirect(reverse('main:home'))
    messages.error(request, errStr)
    return errResponse


@login_required
def saveReport(request,type):
    if request.method == 'POST':
        form = forms.ReportForm(request.POST)
        reportid = request.POST.get('reportid')

        report = get_object_or_404(Report, pk=int(reportid))
        imauthor, imleader, immanager = checkMyRole(request.user.profile, report.author)
        if form.is_valid():
            if imauthor:
                if type in [Report.STATUS_INITIAL, Report.STATUS_SUBMITTOLEADER]:
                    if report.status in [Report.STATUS_INITIAL, Report.STATUS_RETURNBYLEADER]:
                        report.note1 = form.cleaned_data['note']
                        report.status = type
                        report.save()
                        if type == Report.STATUS_SUBMITTOLEADER:
                            if report.extraReports.count() > 0:
                                extraReports = report.extraReports.all()
                                for xr in extraReports:
                                    xr.status = ExtraReport.STATUS_SUBMITTOLEADER
                                    xr.save()
                            else:
                                for department in [u'1',u'2',u'3']:
                                    if request.user.profile.department == department:
                                        pass
                                    else:
                                        x = ExtraReport(leader=department,status=ExtraReport.STATUS_SUBMITTOLEADER)
                                        x.report = report
                                        x.save()
            elif imleader:
                if type in [Report.STATUS_LEADERCHECK,Report.STATUS_RETURNBYLEADER,Report.STATUS_SUBMITTOMANAGER_WAIT]:
                    if report.status in [Report.STATUS_LEADERCHECK, Report.STATUS_RETURNBYMANAGER]:
                        report.scoreL2 = form.cleaned_data['scoreL']
                        report.scoreS2 = form.cleaned_data['scoreS']
                        report.scoreD2 = form.cleaned_data['scoreD']
                        report.scoreR2 = form.cleaned_data['scoreR']

                        report.note2 = form.cleaned_data['note']
                        report.status = type
                        report.save()

                        extraReports = report.extraReports.all()
                        if type == Report.STATUS_SUBMITTOMANAGER_WAIT:
                            n = 0
                            for xr in extraReports:
                                if xr.status == ExtraReport.STATUS_SUBMITTOMANAGER:
                                    n += 1
                            if n == 2:
                                report.status = Report.STATUS_SUBMITTOMANAGER_DONE
                                report.save()
                        elif type == Report.STATUS_RETURNBYLEADER:
                            for xr in extraReports:
                                xr.status = ExtraReport.STATUS_RETURNBYLEADER
                                xr.save()
            elif immanager:
                if type in [Report.STATUS_MANAGERCHECK, Report.STATUS_ARCHIVED, Report.STATUS_RETURNBYMANAGER]:
                    if report.status in [Report.STATUS_MANAGERCHECK]:
                        report.scoreL3 = form.cleaned_data['scoreL']
                        report.scoreS3 = form.cleaned_data['scoreS']
                        report.scoreD3 = form.cleaned_data['scoreD']
                        report.scoreR3 = form.cleaned_data['scoreR']

                        report.note3 = form.cleaned_data['note']

                        report.status = type
                        report.save()

                        extraReports = report.extraReports.all()
                        if type == Report.STATUS_RETURNBYMANAGER:
                            for xr in extraReports:
                                xr.status = ExtraReport.STATUS_RETURNBYMANAGER
                                xr.save()
                        elif type == Report.STATUS_ARCHIVED:
                            for xr in extraReports:
                                xr.status = ExtraReport.STATUS_ARCHIVED
                                xr.save()
                        else:
                            for xr in extraReports:
                                if xr.status == ExtraReport.STATUS_SUBMITTOMANAGER:
                                    xr.status = ExtraReport.STATUS_MANAGERCHECK
                                    xr.save()

    return redirect(reverse('main:home'))

#only change status, not the content,used for 1-0,3-2
@login_required
def retrieveReport(request):
    if request.method == 'POST':
        reportid = request.POST.get('reportid')

        report = get_object_or_404(Report,pk=int(reportid))
        status = report.status
        profile = request.user.profile
        author = report.author
        extraReports = report.extraReports.all()

        if profile.pk == author.pk:
            if status == Report.STATUS_SUBMITTOLEADER:
                report.status= Report.STATUS_INITIAL
                report.save()
        elif profile.userRole==Profile.LEADER and profile.department==author.department:
            if status in [Report.STATUS_SUBMITTOMANAGER_DONE,Report.STATUS_SUBMITTOMANAGER_WAIT]:
                report.status = Report.STATUS_LEADERCHECK
                report.save()
            elif status == Report.STATUS_LEADERCHECK or status == Report.STATUS_RETURNBYMANAGER:
                report.status = Report.STATUS_RETURNBYLEADER
                report.scoreL2 = 0
                report.scoreS2 = 0
                report.scoreD2 = 0
                report.scoreR2 = 0
                report.save()
                for xr in extraReports:
                    xr.status = ExtraReport.STATUS_RETURNBYLEADER
                    xr.save()

        elif profile.userRole==Profile.MANAGER:
            if status == Report.STATUS_MANAGERCHECK:
                report.status = Report.STATUS_RETURNBYMANAGER
                report.scoreL3 = 0
                report.scoreS3 = 0
                report.scoreD3 = 0
                report.scoreR3 = 0
                report.save()
                for xr in extraReports:
                    xr.status = ExtraReport.STATUS_RETURNBYMANAGER
                    xr.save()

    return redirect(reverse('main:home'))


class ReportList(ListView):
    model = Report
    template_name = 'reportListw.html'
    context_object_name = 'report_list'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        type = self.args[0]
        profile = self.request.user.profile

        if self.kwargs.has_key('imauthor'):
            self.imauthor = self.kwargs['imauthor']

            if self.imauthor == u'1':
                if type == u'11':
                    reports = profile.reports.filter(status__in=[u'2', u'3', u'4', u'7'])
                else:
                    reports = profile.reports.filter(status=type)
                self.template_name = 'reportListw.html'
                return reports
            else:
                if profile.userRole==Profile.LEADER:
                    if type == u'3':
                        reports = Report.objects.filter(author__department=profile.department
                                                        ).filter(status__in=[Report.STATUS_SUBMITTOMANAGER_WAIT,Report.STATUS_SUBMITTOMANAGER_DONE])
                        self.template_name = 'reportListl.html'
                        return reports
                    elif type != Report.STATUS_INITIAL and type != Report.STATUS_ARCHIVED:
                        reports = Report.objects.filter(author__department=profile.department
                                                     ).filter(status=type)
                        self.template_name = 'reportListl.html'
                        return reports
                    else:
                        return None
                else:
                    return None

        else:
            dept = self.args[1]
            if profile.userRole == Profile.MANAGER:
                if type in [Report.STATUS_SUBMITTOMANAGER_DONE,Report.STATUS_MANAGERCHECK,Report.STATUS_RETURNBYMANAGER]:
                    reports = Report.objects.filter(author__department=dept
                                                    ).filter(status=type)

                    for r in reports:
                        s1 = (r.author.department, r.getSum2())
                        extraReports = r.extraReports.all()
                        if extraReports.count() == 2:
                            s2 = (extraReports[0].leader, extraReports[0].getSum())
                            s3 = (extraReports[1].leader, extraReports[1].getSum())
                            s = (s1, s2, s3)
                            ss = sorted(s, key=lambda x: x[0])
                            r.dept1Sum = ss[0][1]
                            r.dept2Sum = ss[1][1]
                            r.dept3Sum = ss[2][1]
                            #deptSum = s1[1]*Decimal.from_float(0.5) + s2[1]*Decimal.from_float(0.25) + s3[1]*Decimal.from_float(0.25)
                            # r.sum = deptSum * Decimal.from_float(0.5) + r.getSum3()* Decimal.from_float(0.5)
                            # r.sum = round(r.sum,2)
                            deptSum = getDeptSum(s1[1], s2[1], s3[1])
                            r.sum = getTotalSum(deptSum,r.getSum3())
                        else:
                            if s1[0] == u'1':
                                r.dept1Sum = s1[1]
                                r.dept2Sum = '-'
                                r.dept3Sum = '-'
                            elif s1[0] == u'2':
                                r.dept1Sum = '-'
                                r.dept2Sum = s1[1]
                                r.dept3Sum = '-'
                            else:
                                r.dept1Sum = '-'
                                r.dept2Sum = '-'
                                r.dept3Sum = s1[1]

                            r.sum = r.getSumAll()

                    self.template_name = 'reportListm.html'
                    return reports
                else:
                    return None
            else:
                return None

    def get_context_data(self, **kwargs):
        context = super(ReportList, self).get_context_data(**kwargs)

        ima = False
        if self.kwargs.has_key('imauthor'):
            if self.kwargs['imauthor']=='1':
                ima =True
        # ima = self.imauthor

        if ima:
            if self.args[0] == '0':
                context['title'] = u'未提交'
            elif self.args[0] == '1':
                context['title'] = u'已提交'
            elif self.args[0] == '11':
                context['title'] = u'审核中'
            elif self.args[0] == '5':
                context['title'] = u'已归档'
            elif self.args[0] in ['6', '7']:
                context['title'] = u'被退回'
        else:
            context['title'] = Report.STATUS[int(self.args[0])][1]

        return context

#ss is my dept's score
def getDeptSum(ss,s2,s3):
    return ss*Decimal.from_float(0.5) + s2*Decimal.from_float(0.25) + s3*Decimal.from_float(0.25)

#ds is depts' total, ms is manager's score,return round 2
def getTotalSum(ds,ms):
    s = ds * Decimal.from_float(0.5) + ms * Decimal.from_float(0.5)
    return round(s,2)

@login_required
def getExtraReports(request,type,dept):
    template_name = 'extraReportList.html'
    context ={}
    if type == '1':
        context['title'] = u'已提交科室'
    elif type == '2':
        context['title'] = u'审核中'
    elif type == '3':
        context['title'] = u'已提交部门'
    elif type == '4':
        context['title'] = u'部门审核中'
    elif type == '7':
        context['title'] = u'退回科室'

    reports = []

    rs = ExtraReport.objects.filter(report__author__department=dept
                                         ).filter(status=type).filter(leader=request.user.profile.department)

    for r in rs:
        item = {
            'id':r.pk,
            'author':r.report.author,
            'month':r.report.month,
            'sum':r.getSum()
        }
        reports.append(item)

    context['reports']=reports

    return render(request,template_name,context)


@login_required
def editExtraReport(request,xid):
    xReport = get_object_or_404(ExtraReport,pk=int(xid))
    report = xReport.report

    tasksL = report.tasks.filter(type=u'1')
    tasksS = report.tasks.filter(type=u'2')
    tasksD = report.tasks.filter(type=u'3')

    context={
                'reportmonth': report.month,
                'reportid': xid,
                'tasksL': tasksL,
                'tasksS': tasksS,
                'tasksD': tasksD
            }

    if request.user.profile.userRole == Profile.LEADER:
        if xReport.status in [ExtraReport.STATUS_SUBMITTOLEADER, ExtraReport.STATUS_LEADERCHECK,ExtraReport.STATUS_RETURNBYMANAGER]:
            if xReport.status != ExtraReport.STATUS_RETURNBYMANAGER:
                xReport.status = Report.STATUS_LEADERCHECK
                xReport.save()

            reportForm = forms.ReportForm({
                'scoreL': xReport.scoreL,
                'scoreS': xReport.scoreS,
                'scoreD': xReport.scoreD,
                'scoreR': xReport.scoreR,
            })
            context['reportForm'] = reportForm
            context['note1'] = report.note1
            context['note3'] = report.note3
            context['department'] = report.author.get_department_display()
            context['author'] = report.author
            return render(request, 'editExtraReporte.html', context)
        elif xReport.status in[ExtraReport.STATUS_SUBMITTOMANAGER,ExtraReport.STATUS_MANAGERCHECK]:
            context['scoreL'] = xReport.scoreL
            context['scoreS'] = xReport.scoreS
            context['scoreD'] = xReport.scoreD
            context['scoreR'] = xReport.scoreR
            context['note1'] = report.note1
            context['note3'] = report.note3
            context['author'] = report.author
            context['hasbtn'] = (xReport.status == ExtraReport.STATUS_SUBMITTOMANAGER) and (report.status in [Report.STATUS_SUBMITTOLEADER,Report.STATUS_LEADERCHECK,Report.STATUS_SUBMITTOMANAGER_WAIT,Report.STATUS_SUBMITTOMANAGER_DONE])
            context['department'] = report.author.get_department_display()
            return render(request, 'editExtraReportr.html', context)

    else:
        whenErrorHappens(request, u'无操作权限')

    return redirect(reverse('main:home'))


@login_required
def saveExtraReport(request,type):
    if request.method == 'POST':
        form = forms.ReportForm(request.POST)
        xid = request.POST.get('reportid')

        extraReport = get_object_or_404(ExtraReport, pk=int(xid))
        report = extraReport.report
        if form.is_valid():
            if request.user.profile.userRole == Profile.LEADER:
                if extraReport.status in [ExtraReport.STATUS_SUBMITTOLEADER,ExtraReport.STATUS_LEADERCHECK,ExtraReport.STATUS_RETURNBYMANAGER]:
                    if type in [ExtraReport.STATUS_LEADERCHECK,ExtraReport.STATUS_SUBMITTOMANAGER]:
                        extraReport.scoreL = form.cleaned_data['scoreL']
                        extraReport.scoreS = form.cleaned_data['scoreS']
                        extraReport.scoreD = form.cleaned_data['scoreD']
                        extraReport.scoreR = form.cleaned_data['scoreR']
                        extraReport.status = type
                        extraReport.save()

                        if type == ExtraReport.STATUS_SUBMITTOMANAGER:
                            extraReports = report.extraReports.all()
                            n = 0
                            for xr in extraReports:
                                if xr.status == ExtraReport.STATUS_SUBMITTOMANAGER:
                                    n += 1
                            if n == 2:
                                if report.status == Report.STATUS_SUBMITTOMANAGER_WAIT:
                                    report.status = Report.STATUS_SUBMITTOMANAGER_DONE
                                    report.save()

            else:
                whenErrorHappens(request, u'无操作权限')

    return redirect(reverse('main:home'))


#only change status, not the content,used for 3-2
@login_required
def retrieveExtraReport(request):
    if request.method == 'POST':
        reportid = request.POST.get('reportid')

        xReport = get_object_or_404(ExtraReport,pk=int(reportid))
        report = xReport.report

        if request.user.profile.userRole == Profile.LEADER:
            if xReport.status == ExtraReport.STATUS_SUBMITTOMANAGER:
                if report.status in [Report.STATUS_SUBMITTOLEADER,Report.STATUS_LEADERCHECK,
                                     Report.STATUS_SUBMITTOMANAGER_WAIT,Report.STATUS_SUBMITTOMANAGER_DONE]:
                    xReport.status = ExtraReport.STATUS_LEADERCHECK
                    xReport.save()

                    if report.status == Report.STATUS_SUBMITTOMANAGER_DONE:
                        report.status = Report.STATUS_SUBMITTOMANAGER_WAIT
                        report.save()

    return redirect(reverse('main:home'))


@login_required
def historyView(request):
    template_name = 'history.html'
    return render(request, template_name)


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
    response = render(request,template_name,{'tasks':tasks,'taskEditable':True})
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

    response = render(request, template_name, {'tasks': tasks,'taskEditable':True})
    #this cookie kv will be deleted in the js
    response.set_cookie('tasktype', tasktype)
    return response



def ajaxgetreports(request):
    template_name = 'reportListh.html'
    month = request.POST['month']
    dt = datetime.datetime.strptime(month, "%Y-%m")
    date = datetime.date(dt.year,dt.month,1)
    reports = Report.objects.filter(status=Report.STATUS_ARCHIVED).filter(month=date)

    for r in reports:
        s1 = (r.author.department, r.getSum2())
        extraReports = r.extraReports.all()
        if extraReports.count() == 2:
            s2 = (extraReports[0].leader, extraReports[0].getSum())
            s3 = (extraReports[1].leader, extraReports[1].getSum())
            s = (s1, s2, s3)
            ss = sorted(s, key=lambda x: x[0])
            r.dept1Sum = ss[0][1]
            r.dept2Sum = ss[1][1]
            r.dept3Sum = ss[2][1]
            deptSum = getDeptSum(s1[1], s2[1], s3[1])
            r.sum = getTotalSum(deptSum, r.getSum3())
        else:
            if s1[0] == u'1':
                r.dept1Sum = s1[1]
                r.dept2Sum = '-'
                r.dept3Sum = '-'
            elif s1[0] == u'2':
                r.dept1Sum = '-'
                r.dept2Sum = s1[1]
                r.dept3Sum = '-'
            else:
                r.dept1Sum = '-'
                r.dept2Sum = '-'
                r.dept3Sum = s1[1]

            r.sum = r.getSumAll()

    return render(request, template_name,{'report_list':reports})


@login_required
def toexcel(request):
    month = request.POST['month']

    if month !='':
        dt = datetime.datetime.strptime(month, "%Y-%m")
        date = datetime.date(dt.year, dt.month, 1)
        reports = Report.objects.filter(status=Report.STATUS_ARCHIVED).filter(month=date)

        titles = (u'科室',u'姓名',u'技术开发科评分',u'IT支撑科评分',u'规划发展科评分',u'部门评分',u'总分',)
        file = xlwt.Workbook(encoding='utf8')
        #table = FitSheetWrapper.FitSheetWrapper(file.add_sheet('sheet1'))
        table = file.add_sheet('sheet1')
        for i, e in enumerate(titles):
            table.write(0, i, e)
        row = 1
        for report in reports:
            s1 = (report.author.department, report.getSum2())
            extraReports = report.extraReports.all()
            if extraReports.count() == 2:
                s2 = (extraReports[0].leader, extraReports[0].getSum())
                s3 = (extraReports[1].leader, extraReports[1].getSum())
                s = (s1, s2, s3)
                ss = sorted(s, key=lambda x: x[0])
                report.dept1Sum = ss[0][1]
                report.dept2Sum = ss[1][1]
                report.dept3Sum = ss[2][1]
                deptSum = getDeptSum(s1[1], s2[1], s3[1])
                report.sum = getTotalSum(deptSum, report.getSum3())
            else:
                if s1[0] == u'1':
                    report.dept1Sum = s1[1]
                    report.dept2Sum = '-'
                    report.dept3Sum = '-'
                elif s1[0] == u'2':
                    report.dept1Sum = '-'
                    report.dept2Sum = s1[1]
                    report.dept3Sum = '-'
                else:
                    report.dept1Sum = '-'
                    report.dept2Sum = '-'
                    report.dept3Sum = s1[1]

                report.sum = report.getSumAll()

            table.write(row,0,report.author.get_department_display())
            table.write(row,1,report.author.displayName)
            table.write(row,2,toStr(report.dept1Sum))
            table.write(row,3, toStr(report.dept2Sum))
            table.write(row,4, toStr(report.dept3Sum))
            table.write(row,5,toStr(report.getSum3()))
            table.write(row,6,toStr(report.sum))
            row = row+1

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=scorelist.xls'
        file.save(response)
        return response
    else:
        pass


# 解决excel表中输出None的问题
def toStr(s):
    s = str(s) if s != None else u''
    return s
