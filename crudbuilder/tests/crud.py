from crudbuilder.abstract import BaseCrudBuilder
from crudbuilder.formset import BaseInlineFormset
from crudbuilder.helpers import reverse
from crudbuilder.tests.models import TestModel, TestChildModel


class TestChildInlineFormset(BaseInlineFormset):
    inline_model = TestChildModel
    parent_model = TestModel
    exclude = ['created_by', 'updated_by']


class TestModelCrud(BaseCrudBuilder):
    model = TestModel
    search_fields = ['name']
    tables2_fields = ('name', 'email')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    modelform_excludes = ['created_by']

    def get_success_url(self):
        return reverse('tests-testmodels-detail', args=(self.object.pk,))
