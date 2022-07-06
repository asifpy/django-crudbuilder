import django

try:
    from django.apps import apps
except ImportError:
    pass

from crudbuilder.registry import register
from six import with_metaclass
from django.contrib.contenttypes.models import ContentType

from crudbuilder.exceptions import NotModelException
from crudbuilder import helpers


class BaseBuilder(object):
    def __init__(
            self,
            app,
            model,
            crud
    ):

        self.model = model
        self.app = app
        self.crud = crud

        self.custom_modelform = self._has_crud_attr('custom_modelform')
        self.modelform_excludes = self._has_crud_attr('modelform_excludes')
        self.detailview_excludes = self._has_crud_attr('detailview_excludes')
        self.createupdate_forms = self._has_crud_attr('createupdate_forms')

        self.custom_list_view_mixin = self._has_crud_attr('custom_list_view_mixin')
        self.custom_update_view_mixin = self._has_crud_attr('custom_update_view_mixin')
        self.custom_create_view_mixin = self._has_crud_attr('custom_create_view_mixin')
        self.custom_delete_view_mixin = self._has_crud_attr('custom_delete_view_mixin')

        # django tables2
        self.custom_table2 = self._has_crud_attr('custom_table2')
        self.tables2_fields = self._has_crud_attr('tables2_fields')
        self.tables2_css_class = self._has_crud_attr('tables2_css_class')
        self.tables2_pagination = self._has_crud_attr('tables2_pagination')

        self.permission_required = self._has_crud_attr('permission_required')
        self.permissions = self._has_crud_attr('permissions')
        self.login_required = self._has_crud_attr('login_required')

        self.custom_templates = self._has_crud_attr('custom_templates')
        self.custom_queryset = self._has_crud_attr('custom_queryset')
        self.custom_context = self._has_crud_attr('custom_context')
        self.custom_detail_context = self._has_crud_attr('custom_detail_context')
        self.inlineformset = self.get_inlineformset
        self.custom_postfix_url = self.postfix_url
        self.custom_listview_obj = self._has_crud_attr('custom_listview_obj')

    @property
    def get_model_class(self):
        """Returns model class"""
        try:
            c = ContentType.objects.get(app_label=self.app, model=self.model)
        except ContentType.DoesNotExist:
            # try another kind of resolution
            # fixes a situation where a proxy model is defined in some external app.
            if django.VERSION >= (1, 7):
                return apps.get_model(self.app, self.model)
        else:
            return c.model_class()

    def _has_crud_attr(self, attr):
        return getattr(self.crud, attr, None)

    def view_permission(self, view_type):
        if self.permissions:
            return self.permissions.get(view_type, None)
        else:
            return '{}.{}_{}'.format(self.app, self.model, view_type)

    @property
    def check_login_required(self):
        return True if self.login_required else False

    @property
    def check_permission_required(self):
        return True if self.permission_required else False

    @property
    def get_inlineformset(self):
        if self.crud.inlineformset:
            return self.crud.inlineformset().construct_formset()
        else:
            return None

    @property
    def postfix_url(self):
        return helpers.custom_postfix_url(self.crud(), self.model)


class MetaCrudRegister(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(
            MetaCrudRegister, cls
        ).__new__(cls, clsname, bases, attrs)

        if bases:
            if newclass.model:
                register(newclass.model, newclass)
            else:
                msg = "No model defined in {} class".format(newclass)
                raise NotModelException(msg)
        return newclass


class BaseCrudBuilder(with_metaclass(MetaCrudRegister)):
    model = None
    inlineformset = None
