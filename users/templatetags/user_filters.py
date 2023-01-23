from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    print(field)
    return field.as_widget(attrs={"class": css})
