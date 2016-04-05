from django.forms.models import inlineformset_factory

from crudbuilder.exceptions import NotModelException


class BaseInlineFormset(object):
    extra = 3
    can_delete = True
    inline_model = None
    parent_model = None
    exclude = []
    fields = None
    formfield_callback = None
    fk_name = None
    formset_class = None
    child_form = None

    def construct_formset(self):
        """
        Returns an instance of the inline formset
        """
        if not self.inline_model or not self.parent_model:
            msg = "Parent and Inline models are required in {}".format(self.__class__.__name__)
            raise NotModelException(msg)

        return inlineformset_factory(
            self.parent_model,
            self.inline_model,
            **self.get_factory_kwargs())

    def get_factory_kwargs(self):
        """
        Returns the keyword arguments for calling the formset factory
        """
        kwargs = {}
        kwargs.update({
            'can_delete': self.can_delete,
            'extra': self.extra,
            'exclude': self.exclude,
            'fields': self.fields,
            'formfield_callback': self.formfield_callback,
            'fk_name': self.fk_name,
        })
        if self.formset_class:
            kwargs['formset'] = self.formset_class

        if self.child_form:
            kwargs['form'] = self.child_form
        return kwargs
