from datetime import datetime, timedelta

from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='discount')
def discount(price, discount):
    return price * (100 - discount) / 100


@register.filter(name='is_new')
def is_new(date):
    if datetime.today().date() >= date > (datetime.today() - timedelta(days=7)).date():
        return True
    return False


@register.filter(name="div")
def div(a, b):
    return a / b


@register.filter(name="sub")
def sub(a, b):
    return a - b


@register.filter(name="mul")
def mul(a, b):
    return a * b

