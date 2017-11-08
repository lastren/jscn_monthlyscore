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


@register.inclusion_tag('tasks.html')
def show_tasks(tasks,editable):
    return {'tasks':tasks,'taskEditable':editable}