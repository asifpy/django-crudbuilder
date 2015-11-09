from django.contrib.contenttypes.models import ContentType


class BaseBuilder(object):
    def __init__(
        self,
        app,
        model,
        custom_modelform=None,
        custom_table2=None
        ):

        self.model = model
        self.app = app

        self.custom_modelform = custom_modelform
        self.modelform_excludes = self._has_model_attr('modelform_excludes')
        # django tables2
        self.custom_table2 = custom_table2
        self.tables2_fields = self._has_model_attr('tables2_fields')
        self.tables2_css_class = self._has_model_attr('tables2_css_class')
        self.tables2_pagination = self._has_model_attr('tables2_pagination')
        self.permission_required = self._has_model_attr('permission_required')

    @property
    def get_model_class(self):
        """Returns model class"""

        c = ContentType.objects.get(app_label=self.app, model=self.model)
        return c.model_class()

    def _has_model_attr(self, attr):
        if hasattr(self.get_model_class, attr):
            return getattr(self.get_model_class, attr)
        else:
            return None

    def view_permission(self, view_type):
        if self.permission_required:
            return self.permission_required.get(view_type, None)
        else:
            return '{}.{}_{}'.format(self.app, self.model, view_type)
