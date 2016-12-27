from django.db import models

from crudbuilder.exceptions import (
    NotModelException,
    AlreadyRegistered,
    NotRegistered
)

__all__ = ('CrudBuilderRegistry', 'register', 'registry')


class CrudBuilderRegistry(dict):
    """Dictionary like object representing a collection of objects."""

    @classmethod
    def extract_args(cls, *args):
        """
        Takes any arguments like a model and crud, or just one of
        those, in any order, and return a model and crud.
        """
        model = None
        crudbuilder = None

        for arg in args:
            if issubclass(arg, models.Model):
                model = arg
            else:
                crudbuilder = arg

        return [model, crudbuilder]

    def register(self, *args, **kwargs):
        """
        Register a crud.

        Two unordered arguments are accepted, at least one should be passed:
        - a model,
        - a crudbuilder class
        """

        assert len(args) <= 2, 'register takes at most 2 args'
        assert len(args) > 0, 'register takes at least 1 arg'

        model, crudbuilder = self.__class__.extract_args(*args)

        if not issubclass(model, models.Model):
            msg = "First argument should be Django Model"
            raise NotModelException(msg)

        key = self._class_key(crudbuilder)

        if key in self:
            msg = "Key '{key}' has already been registered.".format(
                key=key
            )
            raise AlreadyRegistered(msg)

        self.__setitem__(key, crudbuilder)
        return crudbuilder

    def _class_key(self, crudbuilder):
        app_label = crudbuilder.model._meta.app_label
        crud_class_name = crudbuilder.get_class_name()
        return '{}-{}'.format(app_label, crud_class_name)

    def unregister(self, crudbuilder):
        key = self._class_key(crudbuilder)
        if key in self:
            self.__delitem__(key)

    def __getitem__(self, name):
        """
        Return the CrudBuilder class registered for this name. If none is
        registered, raise NotRegistered.
        """
        try:
            return super(CrudBuilderRegistry, self).__getitem__(name)
        except KeyError:
            raise NotRegistered(name, self)


registry = CrudBuilderRegistry()


def register(*args, **kwargs):
    """
    Proxy method :py:meth:`CrudBuilderRegistry.register` of the
    :py:data:`registry` module level instance.
    """
    return registry.register(*args, **kwargs)
