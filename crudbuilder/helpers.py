import re
import string

from crudbuilder.exceptions import CrudModuleNotExit

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
                if (text[-2:-1] in vowels) or (text[0] in string.uppercase):
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


# http://www.sqlobject.org/sqlobject/styles.py.html
class Style(object):

    """
    The base Style class, and also the simplest implementation.  No
    translation occurs -- column names and attribute names match,
    as do class names and table names (when using auto class or
    schema generation).
    """

    def __init__(self, pythonAttrToDBColumn=None,
                 dbColumnToPythonAttr=None,
                 pythonClassToDBTable=None,
                 dbTableToPythonClass=None,
                 idForTable=None,
                 longID=False):
        if pythonAttrToDBColumn:
            self.pythonAttrToDBColumn = lambda a, s = self: pythonAttrToDBColumn(
                s, a)
        if dbColumnToPythonAttr:
            self.dbColumnToPythonAttr = lambda a, s = self: dbColumnToPythonAttr(
                s, a)
        if pythonClassToDBTable:
            self.pythonClassToDBTable = lambda a, s = self: pythonClassToDBTable(
                s, a)
        if dbTableToPythonClass:
            self.dbTableToPythonClass = lambda a, s = self: dbTableToPythonClass(
                s, a)
        if idForTable:
            self.idForTable = lambda a, s = self: idForTable(s, a)
        self.longID = longID

    def pythonAttrToDBColumn(self, attr):
        return attr

    def dbColumnToPythonAttr(self, col):
        return col

    def pythonClassToDBTable(self, className):
        return className

    def dbTableToPythonClass(self, table):
        return table

    def idForTable(self, table):
        if self.longID:
            return self.tableReference(table)
        else:
            return 'id'

    def pythonClassToAttr(self, className):
        return lowerword(className)

    def instanceAttrToIDAttr(self, attr):
        return attr + "ID"

    def instanceIDAttrToAttr(self, attr):
        return attr[:-2]

    def tableReference(self, table):
        return table + "_id"


class MixedCaseUnderscoreStyle(Style):

    """
    This is the default style.  Python attributes use mixedCase,
    while database columns use underscore_separated.
    """

    def pythonAttrToDBColumn(self, attr):
        return mixedToUnder(attr)

    def dbColumnToPythonAttr(self, col):
        return underToMixed(col)

    def pythonClassToDBTable(self, className):
        return className[0].lower() \
            + mixedToUnder(className[1:])

    def dbTableToPythonClass(self, table):
        return table[0].upper() \
            + underToMixed(table[1:])

    def pythonClassToDBTableReference(self, className):
        return self.tableReference(self.pythonClassToDBTable(className))

    def tableReference(self, table):
        return table + "_id"

DefaultStyle = MixedCaseUnderscoreStyle


class MixedCaseStyle(Style):

    """
    This style leaves columns as mixed-case, and uses long
    ID names (like ProductID instead of simply id).
    """

    def pythonAttrToDBColumn(self, attr):
        return capword(attr)

    def dbColumnToPythonAttr(self, col):
        return lowerword(col)

    def dbTableToPythonClass(self, table):
        return capword(table)

    def tableReference(self, table):
        return table + "ID"

defaultStyle = DefaultStyle()


def getStyle(soClass, dbConnection=None):
    if dbConnection is None:
        if hasattr(soClass, '_connection'):
            dbConnection = soClass._connection
    if hasattr(soClass.sqlmeta, 'style') and soClass.sqlmeta.style:
        return soClass.sqlmeta.style
    elif dbConnection and dbConnection.style:
        return dbConnection.style
    else:
        return defaultStyle

#
# Text utilities
#
_mixedToUnderRE = re.compile(r'[A-Z]+')


def mixedToUnder(s):
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


def lowerword(s):
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


def underToAllCaps(value):
    """
    >>> underToAllCaps('foo_bar_baz')
    'Foo Bar Baz'
    """
    return ' '.join(map(lambda x: x.title(), value.split('_')))


def import_crud(app):
    '''
    Import moderator module and register all models it contains with moderation
    '''
    from django.utils.importlib import import_module
    import imp

    try:
        app_path = import_module(app).__path__
    except AttributeError:
        return None

    try:
        imp.find_module('crud', app_path)
    except ImportError:
        return None

    module = import_module("%s.crud" % app)

    return module


def auto_discover():
    '''
    Auto register all apps that have module moderator with moderation
    '''
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        import_crud(app)


if __name__ == '__main__':
    print plural('activity')
