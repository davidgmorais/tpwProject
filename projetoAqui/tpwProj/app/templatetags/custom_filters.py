from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.filter(name='discount')
def discount(price, discount):
    return price * (100 - discount) / 100


@register.filter(name='is_new')
def is_new(date):
    if datetime.today().date() >= date > (datetime.today() - timedelta(days=7)).date():
        return True
    return False
