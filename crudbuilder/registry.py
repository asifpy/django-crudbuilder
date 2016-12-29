from django.db import models

from crudbuilder.exceptions import (
    NotModelException,
    AlreadyRegistered,
    NotRegistered
)

from crudbuilder import helpers

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

        key = self._model_key(model, crudbuilder)

        if key in self:
            msg = "Key '{key}' has already been registered.".format(
                key=key
            )
            raise AlreadyRegistered(msg)

        self.__setitem__(key, crudbuilder)
        return crudbuilder

    def _model_key(self, model, crudbuilder):
        app_label = model._meta.app_label
        model_name = model.__name__.lower()
        postfix_url = helpers.custom_postfix_url(crudbuilder(), model_name)
        return '{}-{}-{}'.format(app_label, model_name, postfix_url)

    def unregister(self, model):
        key = self._model_key(model)
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
