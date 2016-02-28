from crudbuilder.abstract import BaseCrudBuilder
from example.models import Person, PersonEmployment
from example.forms import(
    PersonEmployementCreateForm,
    PersonEmployementUpdateForm
)


class PersonCrud(BaseCrudBuilder):
    model = Person
    search_feilds = ['name']
    tables2_fields = ('name', 'email')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    modelform_excludes = ['created_by', 'updated_by']
    login_required = True
    permission_required = True

    # custom_templates = {
    #     'list': 'yourtemplates/template.html'
    # }

    # permissions = {
    #     'list': 'example.person_list',
    #     'create': 'example.person_create'
    # }

    def custom_queryset(self, request, **kwargs):
        return self.model.objects.all()


class PersonEmploymentCrud(BaseCrudBuilder):
    model = PersonEmployment
    tables2_fields = ('year', 'salary', 'medical_allowance')
    search_feilds = ['year', 'person__name']
    tables2_css_class = "table table-bordered table-condensed"
    # custom_modelform = PersonEmploymentForm
    # modelform_excludes = ['person']
    createupdate_forms = {
        'create': PersonEmployementCreateForm,
        'update': PersonEmployementUpdateForm
    }

    def custom_queryset(self, request, **kwargs):
        return self.model.objects.filter(medical_allowance=False)
