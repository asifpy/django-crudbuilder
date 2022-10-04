import re
from math import floor
from django import template
from itertools import chain
from django.template.defaultfilters import stringfilter
from collections import namedtuple

# try:
#     from django.utils.encoding import force_str
# except ImportError:
# from django.utils.encoding import force_unicode as force_str
from django.utils.encoding import force_str

register = template.Library()
Field = namedtuple('Field', 'name verbose_name')
CrudDetail = namedtuple('CrudDetail', ['app', 'model', 'list_url'])


@register.filter
@stringfilter
def undertospaced(value):
    return value.replace("_", " ").title()


@register.filter
def get_value(obj, field):
    try:
        return getattr(obj, 'get_%s_display' % field)()
    except:
        return getattr(obj, field)


@register.filter
def class_name(obj):
    return obj.__class__.__name__


@register.filter
def crud_detail(crud_key):
    app, model, postfix_url = crud_key.split('-', 2)
    list_url = '{}-{}-list'.format(app, postfix_url)
    return CrudDetail(app, model, list_url)


@register.filter
def get_model_fields(obj, detail_exclude=None):
    model = obj.__class__
    excludes = ['pk']

    property_fields = []
    for name in dir(model):
        if name not in excludes and isinstance(
            getattr(model, name, None), property
        ):
            property_fields.append(Field(name=name, verbose_name=name))
    fields = chain(obj._meta.fields, property_fields)

    if detail_exclude:
        fields = [field for field in fields if field.name not in detail_exclude]
    return fields


@register.filter
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    fields = [field.name for field in instance._meta.fields]
    if field_name in fields:
        return instance._meta.get_field(field_name).verbose_name
    else:
        return field_name


@register.filter(is_safe=True)
def label_with_class(value, arg):
    """Style adjustments"""
    return value.label_tag(attrs={'class': arg})


@register.filter(is_safe=True)
def input_with_class(value, arg):
    value.field.widget.attrs['class'] = arg
    return value


@register.filter(is_safe=True)
def inline_objects(object, inline_fk):
    inline_model = inline_fk.model
    related_filter = {inline_fk.name: object}
    return inline_model.objects.filter(**related_filter)


@register.inclusion_tag('crudbuilder/widgets/tables/pagination.html')
def bootstrap_pagination(page, **kwargs):
    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


def get_pagination_context(page, pages_to_show=11,
                           url=None, size=None, extra=None,
                           parameter_name='page'):
    """
    Generate Bootstrap pagination context from a page object
    """
    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        raise ValueError(
            "Pagination pages_to_show should be a positive"
            "integer, you specified {pages}".format(
                pages=pages_to_show)
        )
    num_pages = page.paginator.num_pages
    current_page = page.number
    half_page_num = int(floor(pages_to_show / 2))
    if half_page_num < 0:
        half_page_num = 0
    first_page = current_page - half_page_num
    if first_page <= 1:
        first_page = 1
    if first_page > 1:
        pages_back = first_page - half_page_num
        if pages_back < 1:
            pages_back = 1
    else:
        pages_back = None
    last_page = first_page + pages_to_show - 1
    if pages_back is None:
        last_page += 1
    if last_page > num_pages:
        last_page = num_pages
    if last_page < num_pages:
        pages_forward = last_page + half_page_num
        if pages_forward > num_pages:
            pages_forward = num_pages
    else:
        pages_forward = None
        if first_page > 1:
            first_page -= 1
        if pages_back is not None and pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None
    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)
        # Append proper character to url
    if url:
        # Remove existing page GET parameters
        url = force_str(url)
        url = re.sub(r'\?{0}\=[^\&]+'.format(parameter_name), '?', url)
        url = re.sub(r'\&{0}\=[^\&]+'.format(parameter_name), '', url)
        # Append proper separator
        if '?' in url:
            url += '&'
        else:
            url += '?'
            # Append extra string to url
    if extra:
        if not url:
            url = '?'
        url += force_str(extra) + '&'
    if url:
        url = url.replace('?&', '?')
    # Set CSS classes, see http://getbootstrap.com/components/#pagination
    pagination_css_classes = ['pagination']
    if size == 'small':
        pagination_css_classes.append('pagination-sm')
    elif size == 'large':
        pagination_css_classes.append('pagination-lg')
        # Build context object
    return {
        'bootstrap_pagination_url': url,
        'num_pages': num_pages,
        'current_page': current_page,
        'first_page': first_page,
        'last_page': last_page,
        'pages_shown': pages_shown,
        'pages_back': pages_back,
        'pages_forward': pages_forward,
        'pagination_css_classes': ' '.join(pagination_css_classes),
        'parameter_name': parameter_name,
    }
