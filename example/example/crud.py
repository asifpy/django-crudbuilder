from crudbuilder.abstract import BaseCrudBuilder
from crudbuilder.formset import BaseInlineFormset

from example.models import Person, PersonEmployment
from example.tables import CustomPersonTable
from example.forms import (
    PersonEmployementCreateForm,
    PersonEmployementUpdateForm
)


class PersonEmploymentInlineFormset(BaseInlineFormset):
    inline_model = PersonEmployment
    parent_model = Person
    exclude = ['created_by', 'updated_by']


class PersonCrud(BaseCrudBuilder):
    model = Person
    search_fields = ['name']
    tables2_fields = ('name', 'email')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 10  # default is 10
    modelform_excludes = ['created_by', 'updated_by']
    login_required = True
    permission_required = True
    # custom_table2 = CustomPersonTable

    # detailview_excludes = ['img']
    # inlineformset = PersonEmploymentInlineFormset

    # custom_templates = {
    #     'list': 'yourtemplates/template.html'
    # }

    # permissions = {
    #     'list': 'example.person_list',
    #     'create': 'example.person_create'
    # }

    # @classmethod
    # def custom_queryset(cls, request, **kwargs):
    #     return cls.model.objects.filter(created_by=request.user)


class AnotherPersonCrud(BaseCrudBuilder):
    model = Person
    tables2_css_class = "table table-bordered table-condensed"
    custom_postfix_url = 'another-person-crud'  # /appname/<custom_postfix_url>


class PersonEmploymentCrud(BaseCrudBuilder):
    model = PersonEmployment
    tables2_fields = ('year', 'salary', 'medical_allowance')
    search_fields = ['year', 'person__name']
    tables2_css_class = "table table-bordered table-condensed"
    # custom_modelform = PersonEmploymentForm
    # modelform_excludes = ['person']
    createupdate_forms = {
        'create': PersonEmployementCreateForm,
        'update': PersonEmployementUpdateForm
    }

    @classmethod
    def custom_queryset(cls, request, **kwargs):
        return cls.model.objects.filter(medical_allowance=False)
