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
    CreateUpdateViewMixin,
    InlineFormsetViewMixin,
    BaseDetailViewMixin
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

    def get_actual_form(self, view):
        if self.createupdate_forms and self.createupdate_forms.get(view, None):
            return self.createupdate_forms.get(view)
        elif self.custom_modelform:
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
        """Generate modelform from Django modelform_factory"""

        model_class = self.get_model_class
        excludes = self.modelform_excludes if self.modelform_excludes else []
        _ObjectForm = modelform_factory(model_class, exclude=excludes)
        return _ObjectForm

    def get_template(self, tname):
        """
        - Get custom template from CRUD class, if it is defined in it
        - No custom template in CRUD class, then use the default template
        """

        if self.custom_templates and self.custom_templates.get(tname, None):
            return self.custom_templates.get(tname)
        elif self.inlineformset:
            return 'inline/{}.html'.format(tname)
        else:
            return 'instance/{}.html'.format(tname)

    def get_createupdate_mixin(self):
        if self.inlineformset:
            return InlineFormsetViewMixin
        else:
            return CreateUpdateViewMixin

    def generate_list_view(self):
        """Generate class based view for ListView"""

        name = model_class_form(self.model + 'ListView')
        list_args = dict(
            model=self.get_model_class,
            context_object_name=plural(self.model),
            template_name=self.get_template('list'),
            table_class=self.get_actual_table(),
            context_table_name='table_objects',
            crud=self.crud,
            permissions=self.view_permission('list'),
            permission_required=self.check_permission_required,
            login_required=self.check_login_required,
            table_pagination={'per_page': self.tables2_pagination or 10},
            custom_queryset=self.custom_queryset,
            custom_context=self.custom_context
        )

        list_class = type(
            name,
            (BaseListViewMixin, SingleTableView),
            list_args
        )
        self.classes[name] = list_class
        return list_class

    def generate_create_view(self):
        """Generate class based view for CreateView"""

        name = model_class_form(self.model + 'CreateView')
        create_args = dict(
            form_class=self.get_actual_form('create'),
            model=self.get_model_class,
            template_name=self.get_template('create'),
            permissions=self.view_permission('create'),
            permission_required=self.check_permission_required,
            login_required=self.check_login_required,
            inlineformset=self.inlineformset,
            success_url=reverse_lazy('{}-{}-list'.format(self.app, self.model)),
            custom_form=self.createupdate_forms or self.custom_modelform
        )

        create_class = type(
            name,
            (self.get_createupdate_mixin(), CreateView),
            create_args
        )

        self.classes[name] = create_class
        return create_class

    def generate_detail_view(self):
        """Generate class based view for DetailView"""

        name = model_class_form(self.model + 'DetailView')
        detail_args = dict(
            detailview_excludes = self.detailview_excludes,
            model=self.get_model_class,
            template_name=self.get_template('detail'),
            login_required=self.check_login_required,
            permissions=self.view_permission('detail'),
            inlineformset=self.inlineformset,
            permission_required=self.check_permission_required,
        )

        detail_class = type(name, (BaseDetailViewMixin, DetailView), detail_args)
        self.classes[name] = detail_class
        return detail_class

    def generate_update_view(self):
        """Generate class based view for UpdateView"""

        name = model_class_form(self.model + 'UpdateView')
        update_args = dict(
            form_class=self.get_actual_form('update'),
            model=self.get_model_class,
            template_name=self.get_template('update'),
            permissions=self.view_permission('update'),
            permission_required=self.check_permission_required,
            login_required=self.check_login_required,
            inlineformset=self.inlineformset,
            custom_form=self.createupdate_forms or self.custom_modelform,
            success_url=reverse_lazy('{}-{}-list'.format(self.app, self.model))
        )

        update_class = type(
            name,
            (self.get_createupdate_mixin(), UpdateView),
            update_args
        )
        self.classes[name] = update_class
        return update_class

    def generate_delete_view(self):
        """Generate class based view for DeleteView"""

        name = model_class_form(self.model + 'DeleteView')
        delete_args = dict(
            model=self.get_model_class,
            template_name=self.get_template('delete'),
            permissions=self.view_permission('delete'),
            permission_required=self.check_permission_required,
            login_required=self.check_login_required,
            success_url=reverse_lazy('{}-{}-list'.format(self.app, self.model))
        )

        delete_class = type(name, (CrudBuilderMixin, DeleteView), delete_args)
        self.classes[name] = delete_class
        return delete_class
