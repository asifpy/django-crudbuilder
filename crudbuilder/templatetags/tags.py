from django import template
from itertools import chain
from django.template.defaultfilters import stringfilter
from collections import namedtuple

register = template.Library()
Field = namedtuple('Field', 'name verbose_name')


@register.filter
@stringfilter
def undertospaced(value):
    return value.replace("_", " ").title()


@register.filter
def get_value(obj, field):
    return getattr(obj, field)


@register.filter
def get_model_fields(obj):
    model = obj.__class__
    excludes = ['pk']

    property_fields = []
    for name in dir(model):
        if name not in excludes and isinstance(getattr(model, name), property):
            property_fields.append(Field(name=name, verbose_name=name))

    return chain(obj._meta.fields, property_fields)
