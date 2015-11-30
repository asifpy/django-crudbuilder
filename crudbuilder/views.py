from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.views.generic import(
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django_tables2 import SingleTableView

from crudbuilder.mixins import(
    CrudBuilderMixin,
    BaseListViewMixin,
    CreateUpdateViewMixin
)
from crudbuilder.abstract import BaseBuilder
from crudbuilder.tables import TableBuilder
from crudbuilder.helpers import model_class_form, plural


class ViewBuilder(BaseBuilder):
    """View builder which returns all the CRUD class based views"""

    def __init__(self, *args, **kwargs):
        super(ViewBuilder, self).__init__(*args, **kwargs)
        self.classes = {}

    def generate_crud(self):
        self.generate_list_view()
        self.generate_create_view()
        self.generate_detail_view()
        self.generate_update_view()
        self.generate_delete_view()

    def get_actual_form(self):
        if self.custom_modelform:
            return self.custom_modelform
        else:
            return self.generate_modelform()

    def get_actual_table(self):
        if self.custom_table2:
            return self.custom_table2
        else:
            table_builder = TableBuilder(self.app, self.model, self.crud)
            return table_builder.generate_table()

    def generate_modelform(self):
        model_class = self.get_model_class
        excludes = self.modelform_excludes if self.modelform_excludes else []
        _ObjectForm = modelform_factory(model_class, exclude=excludes)
        return _ObjectForm

    def generate_list_view(self):
        name = model_class_form(self.model + 'ListView')
        list_args = dict(
            model=self.get_model_class,
            context_object_name=plural(self.model),
            template_name='object_list.html',
            table_class=self.get_actual_table(),
            context_table_name='table_objects',
            crud=self.crud,
            permission_required=self.view_permission('list'),
            table_pagination=self.tables2_pagination or 10
            )

        list_class = type(
            name,
            (BaseListViewMixin, SingleTableView),
            list_args
            )
        self.classes[name] = list_class
        return list_class

    def generate_create_view(self):
        name = model_class_form(self.model + 'CreateView')
        create_args = dict(
            form_class=self.get_actual_form(),
            model=self.get_model_class,
            template_name='object_create.html',
            permission_required=self.view_permission('create'),
            success_url=reverse_lazy('{}-{}-list'.format(self.app, self.model))
            )

        create_class = type(name, (CreateUpdateViewMixin, CreateView), create_args)
        self.classes[name] = create_class
        return create_class

    def generate_detail_view(self):
        name = model_class_form(self.model + 'DetailView')
        detail_args = dict(
            model=self.get_model_class,
            template_name='object_detail.html',
            permission_required=self.view_permission('detail')
            )

        detail_class = type(name, (CrudBuilderMixin, DetailView), detail_args)
        self.classes[name] = detail_class
        return detail_class

    def generate_update_view(self):
        name = model_class_form(self.model + 'UpdateView')
        update_args = dict(
            form_class=self.get_actual_form(),
            model=self.get_model_class,
            template_name='object_update.html',
            permission_required=self.view_permission('update'),
            success_url=reverse_lazy('{}-{}-list'.format(self.app, self.model))
            )

        update_class = type(
            name,
            (CreateUpdateViewMixin, UpdateView),
            update_args
            )
        self.classes[name] = update_class
        return update_class

    def generate_delete_view(self):
        name = model_class_form(self.model + 'DeleteView')
        delete_args = dict(
            model=self.get_model_class,
            template_name='object_delete.html',
            permission_required=self.view_permission('delete'),
            success_url=reverse_lazy('{}-{}-list'.format(self.app, self.model))
            )

        delete_class = type(name, (CrudBuilderMixin, DeleteView), delete_args)
        self.classes[name] = delete_class
        return delete_class
