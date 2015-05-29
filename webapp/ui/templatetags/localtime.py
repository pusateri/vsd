from django import template
from settings import TIME_ZONE
from pytz import timezone, utc
import datetime

register = template.Library()

@register.filter
def localtime(dt):
    tz = timezone(TIME_ZONE)
    loc = dt.replace(tzinfo=utc).astimezone(tz)
    return loc