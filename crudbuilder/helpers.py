
import re
import string
import imp

try:
    # Django versions >= 1.9
    from django.utils.module_loading import import_module
except ImportError:
    # Django versions < 1.9
    from django.utils.importlib import import_module


__all__ = ['plural', 'mixedToUnder', 'capword', 'lowerword', 'underToMixed']

# http://code.activestate.com/recipes/82102-smart-pluralisation-english/


def plural(text):
    """
        >>> plural('activity')
        'activities'
    """
    aberrant = {
        'knife': 'knives',
        'self': 'selves',
        'elf': 'elves',
        'life': 'lives',
        'hoof': 'hooves',
        'leaf': 'leaves',
        'echo': 'echoes',
        'embargo': 'embargoes',
        'hero': 'heroes',
        'potato': 'potatoes',
        'tomato': 'tomatoes',
        'torpedo': 'torpedoes',
        'veto': 'vetoes',
        'child': 'children',
        'woman': 'women',
        'man': 'men',
        'person': 'people',
        'goose': 'geese',
        'mouse': 'mice',
        'barracks': 'barracks',
        'deer': 'deer',
        'nucleus': 'nuclei',
        'syllabus': 'syllabi',
        'focus': 'foci',
        'fungus': 'fungi',
        'cactus': 'cacti',
        'phenomenon': 'phenomena',
        'index': 'indices',
        'appendix': 'appendices',
        'criterion': 'criteria',


    }

    if text in aberrant:
        result = '%s' % aberrant[text]
    else:
        postfix = 's'
        if len(text) > 2:
            vowels = 'aeiou'
            if text[-2:] in ('ch', 'sh'):
                postfix = 'es'
            elif text[-1:] == 'y':
                if (text[-2:-1] in vowels) or (text[0] in string.ascii_uppercase):
                    postfix = 's'
                else:
                    postfix = 'ies'
                    text = text[:-1]
            elif text[-2:] == 'is':
                postfix = 'es'
                text = text[:-2]
            elif text[-1:] in ('s', 'z', 'x'):
                postfix = 'es'

        result = '%s%s' % (text, postfix)
    return result


# Text utilities
#
_mixedToUnderRE = re.compile(r'[A-Z]+')


def mixedToUnder(s):  # pragma: no cover
    """
    Sample:
        >>> mixedToUnder("FooBarBaz")
        'foo_bar_baz'

    Special case for ID:
        >>> mixedToUnder("FooBarID")
        'foo_bar_id'
    """
    if s.endswith('ID'):
        return mixedToUnder(s[:-2] + "_id")
    trans = _mixedToUnderRE.sub(mixedToUnderSub, s)
    if trans.startswith('_'):
        trans = trans[1:]
    return trans


def mixedToUnderSub(match):
    m = match.group(0).lower()
    if len(m) > 1:
        return '_%s_%s' % (m[:-1], m[-1])
    else:
        return '_%s' % m


def capword(s):
    """
    >>> capword('foo')
    'Foo'
    """
    return s[0].upper() + s[1:]


def lowerword(s):  # pragma: no cover
    """
    >>> lowerword('Hello')
    'hello'
    """
    return s[0].lower() + s[1:]

_underToMixedRE = re.compile('_.')


def underToMixed(name):
    """
    >>> underToMixed('some_large_model_name_perhaps')
    'someLargeModelNamePerhaps'

    >>> underToMixed('exception_for_id')
    'exceptionForID'
    """
    if name.endswith('_id'):
        return underToMixed(name[:-3] + "ID")
    return _underToMixedRE.sub(lambda m: m.group(0)[1].upper(),
                               name)


def model_class_form(name):
    """
    >>> model_class_form('foo_bar_baz')
    'FooBarBaz'
    """
    return capword(underToMixed(name))


def underToAllCaps(value):  # pragma: no cover
    """
    >>> underToAllCaps('foo_bar_baz')
    'Foo Bar Baz'
    """
    return ' '.join(map(lambda x: x.title(), value.split('_')))


def import_crud(app):
    '''
    Import crud module and register all model cruds which it contains
    '''

    try:
        app_path = import_module(app).__path__
    except (AttributeError, ImportError):
        return None

    try:
        imp.find_module('crud', app_path)
    except ImportError:
        return None

    module = import_module("%s.crud" % app)

    return module


def auto_discover():
    '''
    Auto register all apps that have module crud
    '''
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        import_crud(app)


def custom_postfix_url(crud, model):
    postfix = getattr(crud, 'custom_postfix_url', None)

    if not postfix:
        postfix = plural(model)
    return postfix


def get_urlresolver():
    """Returns apporpriate urlresolver based on django version"""

    try:
        from django.core import urlresolvers
        return urlresolvers
    except ImportError:
        from django import urls
        return urls


reverse_lazy = get_urlresolver().reverse_lazy
reverse = get_urlresolver().reverse
