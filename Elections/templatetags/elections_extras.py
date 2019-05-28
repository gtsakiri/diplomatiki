from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter
def index(List, i):
    return List[int(i)]