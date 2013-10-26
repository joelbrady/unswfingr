from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def space_split(str):
    return str.split(' ')


@register.filter
@stringfilter
def dot_split(str):
    return str.split('.')
