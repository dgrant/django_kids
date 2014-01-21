from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    if value == None:
        return False
    else:
        return value.startswith(arg)
