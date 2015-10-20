import os

from django import forms
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from crudbuilder.text import model_class_form, plural


from django.views.generic import(
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


class ViewBuilder(object):

    def __init__(self, model, excludes=None, custom_form=None, autocomplete_fields=None):
        self.model = model
        self.excludes = excludes
        self.custom_form = custom_form
        self.autocomplete_fields = autocomplete_fields
        self.classes = {}

    def get_model_class(self):
        c = ContentType.objects.get(model=self.model)
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
                exclude = []
                autocomplete_fields = self.autocomplete_fields

            def __init__(self, *args, **kwargs):
                self.helper = FormHelper()
                self.helper.form_method = 'post'
                self.helper.form_tag = True
                self.helper.form_class = 'form-horizontal'
                self.helper.label_class = 'col-sm-2 control-label'
                self.helper.field_class = 'col-sm-3'
                self.helper.add_input(
                    Submit('submit', 'Submit',
                        css_class="col-sm-offset-2 btn-primary"
                        )
                    )
                super(_ObjectForm, self).__init__(*args, **kwargs)
        return _ObjectForm

    def generate_list_view(self):
        name = model_class_form(self.model + 'ListView')

        list_class = type(name, (ListView,), {
            'model': self.get_model_class(),
            'context_object_name': plural(self.model),
            'template_name': 'object_list.html',
        })

        self.classes[name] = list_class
        return list_class

    def generate_create_view(self):
        name = model_class_form(self.model + 'CreateView')

        
        create_class = type(name, (CreateView,), {
            'form_class': self.get_actual_form(),
            'template_name': 'object_create.html',
            'success_url': reverse_lazy('{}-list'.format(self.model))
        })
        self.classes[name] = create_class
        return create_class

    def generate_detail_view(self):
        name = model_class_form(self.model + 'DetailView')

        detail_class = type(name, (DetailView,), {
            'model': self.get_model_class(),
            'template_name': 'object_detail.html',
        })
        self.classes[name] = detail_class
        return detail_class

    def generate_update_view(self):
        name = model_class_form(self.model + 'UpdateView')

        update_class= type(name, (UpdateView,), {
            'form_class': self.get_actual_form(),
            'model': self.get_model_class(),
            'template_name': 'object_update.html',
            'success_url': reverse_lazy('{}-list'.format(self.model))
        })
        self.classes[name] = update_class
        return update_class

    def generate_delete_view(self):
        name = model_class_form(self.model + 'DeleteView')

        delete_class = type(name, (DeleteView,), {
            'model': self.get_model_class(),
            'template_name':  'object_delete.html',
            'success_url': reverse_lazy('{}-list'.format(self.model))
            })

        self.classes[name] = delete_class
        return delete_class

# if __name__ == '__main__':
#     builder = ViewBuilder('pipe')
#     builder.generate_list_view()
#     print builder.classes
