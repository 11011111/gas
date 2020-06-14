from django import template

from gas.person.models import WorkTime

register = template.Library()


@register.simple_tag(name='get_workers')
def get_workers(station, date):
    try:
        return WorkTime.objects.filter(station=station, DTS__day=date.day, DTS__month=date.month, DTS__year=date.year)
    except:
        return []
