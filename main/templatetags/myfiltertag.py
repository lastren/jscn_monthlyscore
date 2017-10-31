from django import template
import datetime

register = template.Library()

@register.filter
def month2str(value):
    return value.strftime('%Y-%m')

@register.simple_tag(takes_context=True)
def current_reportid(context):
    value = context['timezone']
    return value


@register.inclusion_tag('results.html')
def show_results(report):
    tasks = report.tasks.all()