# -*- coding: UTF-8 -*-
from accounts.models import Profile
from django.contrib.auth.models import User
from main.models import Report,ExtraReport
from django.http import request

def reportNumContextProc(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return{}
        data = getReportNum(request.user)
        return data
    else:
        return {}


def getReportNum(account):
    result = {}
    user = User.objects.get(username=account)
    profile = user.profile
    role = profile.userRole

    if role == Profile.WORKER:
        result['w0'] = profile.reports.filter(status=Report.STATUS_INITIAL).count()
        result['w1'] = profile.reports.filter(status=Report.STATUS_SUBMITTOLEADER).count()
        result['w11'] = profile.reports.filter(status__in=[u'2', u'3', u'4', u'7']).count()
        result['w6'] = profile.reports.filter(status=Report.STATUS_RETURNBYLEADER).count()
    elif role == Profile.LEADER:
        reports = Report.objects.filter(author__department=profile.department)
        result['l1'] = reports.filter(status=Report.STATUS_SUBMITTOLEADER).count()
        result['l2'] = reports.filter(status=Report.STATUS_LEADERCHECK).count()
        result['l3'] = reports.filter(status__in=[Report.STATUS_SUBMITTOMANAGER_WAIT, Report.STATUS_SUBMITTOMANAGER_DONE]).count()
        result['l4'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['l6'] = reports.filter(status=Report.STATUS_RETURNBYLEADER).count()
        result['l7'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()

        xreport1 = ExtraReport.objects.filter(report__author__department=Profile.DP1)
        #123,1author's department,2leader's department,3extrareport's status
        result['l111'] = xreport1.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l112'] = xreport1.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l113'] = xreport1.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l114'] = xreport1.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l117'] = xreport1.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()
        result['l121'] = xreport1.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l122'] = xreport1.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l123'] = xreport1.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l124'] = xreport1.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l127'] = xreport1.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()
        result['l131'] = xreport1.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l132'] = xreport1.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l133'] = xreport1.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l134'] = xreport1.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l137'] = xreport1.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()

        xreport2 = ExtraReport.objects.filter(report__author__department=Profile.DP2)
        result['l211'] = xreport2.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l212'] = xreport2.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l213'] = xreport2.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l214'] = xreport2.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l217'] = xreport2.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()
        result['l221'] = xreport2.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l222'] = xreport2.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l223'] = xreport2.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l224'] = xreport2.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l227'] = xreport2.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()
        result['l231'] = xreport2.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l232'] = xreport2.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l233'] = xreport2.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l234'] = xreport2.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l237'] = xreport2.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()

        xreport3 = ExtraReport.objects.filter(report__author__department=Profile.DP3)
        result['l311'] = xreport3.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l312'] = xreport3.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l313'] = xreport3.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l314'] = xreport3.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l317'] = xreport3.filter(leader=ExtraReport.DP1).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()
        result['l321'] = xreport3.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l322'] = xreport3.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l323'] = xreport3.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l324'] = xreport3.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l327'] = xreport3.filter(leader=ExtraReport.DP2).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()
        result['l331'] = xreport3.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_SUBMITTOLEADER).count()
        result['l332'] = xreport3.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_LEADERCHECK).count()
        result['l333'] = xreport3.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_SUBMITTOMANAGER).count()
        result['l334'] = xreport3.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_MANAGERCHECK).count()
        result['l337'] = xreport3.filter(leader=ExtraReport.DP3).filter(status=ExtraReport.STATUS_RETURNBYMANAGER).count()
    elif role == Profile.MANAGER:
        reports = Report.objects.filter(author__department=Profile.DP1)
        result['m31'] = reports.filter(status=Report.STATUS_SUBMITTOMANAGER_DONE).count()
        result['m41'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['m71'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()

        reports = Report.objects.filter(author__department=Profile.DP2)
        result['m32'] = reports.filter(status=Report.STATUS_SUBMITTOMANAGER_DONE).count()
        result['m42'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['m72'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()

        reports = Report.objects.filter(author__department=Profile.DP3)
        result['m33'] = reports.filter(status=Report.STATUS_SUBMITTOMANAGER_DONE).count()
        result['m43'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['m73'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()

    return result