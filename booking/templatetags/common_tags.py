from django import template
import datetime

register = template.Library()


@register.simple_tag
def calc_date_from_now(format, days):
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=days)
    return tomorrow_date.strftime(format)


@register.simple_tag
def get_date(year, month, day):
    return datetime.datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
    # return date.weekday()

