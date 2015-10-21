import os

from django import forms
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.views.generic import(
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from crudbuilder.mixins import CrudBuilderMixin
from crudbuilder.text import model_class_form, plural

class ViewBuilder(object):

    def __init__(self, app, model, excludes=None, custom_form=None):
        self.model = model
        self.app = app
        self.excludes = excludes
        self.custom_form = custom_form
        self.classes = {}

    def get_model_class(self):
        c = ContentType.objects.get(app_label=self.app, model=self.model)
        return c.model_class()

    def get_actual_form(self):
        if self.custom_form:
            return self.custom_form
        else:
            return self.generate_modelform()

    def generate_modelform(self):
        model_class = self.get_model_class()
        class _ObjectForm(forms.ModelForm):
            class Meta:
                model = model_class
                exclude = self.excludes if self.excludes else []

        return _ObjectForm

    def generate_list_view(self):
        name = model_class_form(self.model + 'ListView')

        list_class = type(name, (CrudBuilderMixin, ListView), {
            'model': self.get_model_class(),
            'context_object_name': plural(self.model),
            'template_name': 'object_list.html',
        })

        self.classes[name] = list_class
        return list_class

    def generate_create_view(self):
        name = model_class_form(self.model + 'CreateView')

        create_class = type(name, (CrudBuilderMixin, CreateView), {
            'form_class': self.get_actual_form(),
            'model': self.get_model_class(),
            'template_name': 'object_create.html',
            'success_url': reverse_lazy('{}-{}-list'.format(self.app, self.model))
        })
        self.classes[name] = create_class
        return create_class

    def generate_detail_view(self):
        name = model_class_form(self.model + 'DetailView')

        detail_class = type(name, (CrudBuilderMixin, DetailView), {
            'model': self.get_model_class(),
            'template_name': 'object_detail.html',
        })
        self.classes[name] = detail_class
        return detail_class

    def generate_update_view(self):
        name = model_class_form(self.model + 'UpdateView')

        update_class= type(name, (CrudBuilderMixin, UpdateView), {
            'form_class': self.get_actual_form(),
            'model': self.get_model_class(),
            'template_name': 'object_update.html',
            'success_url': reverse_lazy('{}-{}-list'.format(self.app, self.model))
        })
        self.classes[name] = update_class
        return update_class

    def generate_delete_view(self):
        name = model_class_form(self.model + 'DeleteView')

        delete_class = type(name, (CrudBuilderMixin, DeleteView), {
            'model': self.get_model_class(),
            'template_name':  'object_delete.html',
            'success_url': reverse_lazy('{}-{}-list'.format(self.app, self.model))
            })

        self.classes[name] = delete_class
        return delete_class

# if __name__ == '__main__':
#     builder = ViewBuilder('pipe')
#     builder.generate_list_view()
#     print builder.classes
