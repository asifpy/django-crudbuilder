from django import template
from django.contrib import admin
from django.template.defaultfilters import stringfilter
from itertools import cycle, chain

from crudbuilder.text import mixedToUnder, plural

register = template.Library()

@register.filter
def get_model_fields(obj):
    model = obj.__class__
    excludes = ['pk']

    property_fields = []
    for name in dir(model):
        if name not in excludes and isinstance(getattr(model, name), property):
            property_fields.append(Field(name=name, verbose_name=name))

    return chain(obj._meta.fields, property_fields)

@register.filter
def get_verbose_name(obj, field_name):
    try:
        return obj._meta.get_field(field_name).verbose_name
    except FieldDoesNotExist:
        return ''

@register.filter
def get_value(obj, field):
    return getattr(obj, field)

@register.filter
def get_model_for_queryset(queryset):
    model_name = queryset.model.__name__
    return mixedToUnder(model_name)


@register.filter
def get_model_for_instance(instance):
    return mixedToUnder(instance.__class__.__name__)


@register.filter
def get_model_for_form(form):
    return mixedToUnder(form.instance.__class__.__name__)


@register.filter
def make_plural(name):
    return plural(name)


@register.filter
def get_field_type(field):
    return field.field.__class__.__name__


@register.filter
def list_display(queryset):
    try:
        return admin.site._registry[queryset.model].list_display
    except AttributeError:
        return tuple()


@register.filter
def get_field(obj, field, default=''):
    display = admin.site._registry[obj.__class__].list_display
    first = display[0] == field

    try:
        field_value = getattr(obj, field) or default
        if first and field_value:
            return field_value
        elif first and not field_value:
            return '(None)'
#        elif isinstance(field_value, models.Model):
# return '<a href="{0}">{1}</a>'.format(field_value.get_absolute_url(),
# field_value)
        else:
            return field_value
    except AttributeError:
        return default

@register.filter
@stringfilter
def undertospaced(value):
    return value.replace("_", " ").title()

