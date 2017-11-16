# -*- coding: UTF-8 -*-
from accounts.models import Profile
from django.contrib.auth.models import User
from main.models import Report
from django.http import request

def reportNumContextProc(request):
    if request.user.is_authenticated:
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
        result['l3'] = reports.filter(status=Report.STATUS_SUBMITTOMANAGER).count()
        result['l4'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['l6'] = reports.filter(status=Report.STATUS_RETURNBYLEADER).count()
        result['l7'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()
    elif role == Profile.MANAGER:
        reports = Report.objects.filter(author__department=Profile.DP1)
        result['m31'] = reports.filter(status=Report.STATUS_SUBMITTOMANAGER).count()
        result['m41'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['m71'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()

        reports = Report.objects.filter(author__department=Profile.DP2)
        result['m32'] = reports.filter(status=Report.STATUS_SUBMITTOMANAGER).count()
        result['m42'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['m72'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()

        reports = Report.objects.filter(author__department=Profile.DP3)
        result['m33'] = reports.filter(status=Report.STATUS_SUBMITTOMANAGER).count()
        result['m43'] = reports.filter(status=Report.STATUS_MANAGERCHECK).count()
        result['m73'] = reports.filter(status=Report.STATUS_RETURNBYMANAGER).count()

    return result