from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.template import Context, Template
from django.test.utils import override_settings

from crudbuilder.helpers import reverse
from crudbuilder.tests.models import TestModel
from crudbuilder.tests.crud import TestModelCrud, TestChildInlineFormset
from crudbuilder.tests.forms import TestModelForm
from crudbuilder.tests.tables import TestModelTable


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        TestModelCrud.custom_modelform = TestModelForm
        TestModelCrud.custom_table2 = TestModelTable

        self.user = User.objects.create_user(
            username='asdf',
            password='asdf3452',
            email='sa@me.org')

    def client_login(self):
        self.client.login(
            username=self.user.username,
            password='asdf3452'
        )

    def get_list_view(self):
        self.client_login()
        response = self.client.get(reverse('tests-testmodels-list'))
        self.assertEqual(200, response.status_code)

    def get_detail_view(self, obj):
        self.client_login()
        response = self.client.get(reverse('tests-testmodels-detail', args=(obj.pk, )))
        self.assertEqual(200, response.status_code)

    def test_user_not_logged_in(self):
        response = self.client.get(reverse('tests-testmodels-list'))
        self.assertEqual(302, response.status_code)

    def tearDown(self):
        TestModelCrud.custom_table2 = None
        TestModelCrud.custom_modelform = None
        TestModelCrud.createupdate_forms = None

    def test_user_logged_in(self):
        self.get_list_view()

    def test_view_with_default_form(self):
        TestModelCrud.custom_modelform = None
        self.get_list_view()

    def test_view_with_default_tables2(self):
        TestModelCrud.custom_table2 = None
        self.get_list_view()

    def test_invalid_entry_create(self):
        self.client_login()
        data = {'name': 'Test text', 'email': 'same.org'}
        response = self.client.post('/crud/tests/testmodels/create/', data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "email", "Enter a valid email address.")

    def test_valid_entry_create(self):
        self.client_login()
        data = {'name': 'Test text', 'email': 'sa@me.org'}
        self.assertEqual(TestModel.objects.count(), 0)

        response = self.client.post('/crud/tests/testmodels/create/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TestModel.objects.count(), 1)

        response = self.client.post('/crud/tests/testmodels/1/update/', data)
        self.assertEqual(response.status_code, 302)

    @override_settings(PERMISSION_REQUIRED_FOR_CRUD=True)
    def test_permission_required_enabled(self):
        self.client_login()
        response = self.client.get('/crud/tests/testmodels/')
        self.assertEqual(302, response.status_code)

    def test_search_list(self):
        self.client_login()
        response = self.client.get('/crud/tests/testmodels/?search=some_text')
        self.assertEqual(200, response.status_code)

    @override_settings(LOGIN_REQUIRED_FOR_CRUD=False)
    def test_no_login(self):
        response = self.client.get(reverse('tests-testmodels-list'))
        self.assertEqual(200, response.status_code)

    def test_separate_createupdateform(self):
        TestModelCrud.custom_modelform = None
        TestModelCrud.createupdate_forms = dict(
            create=TestModelForm,
            update=TestModelForm)

        self.client_login()
        data = {'name': 'Test text', 'email': 'sa@me.org'}
        self.assertEqual(TestModel.objects.count(), 0)

        response = self.client.post('/crud/tests/testmodels/create/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TestModel.objects.count(), 1)

        response = self.client.post('/crud/tests/testmodels/1/update/', data)
        self.assertEqual(response.status_code, 302)

    def test_custom_queryset(self):
        def custom_queryset(self, request, **kwargs):
            return self.model.objects.all()
        setattr(TestModelCrud, 'custom_queryset', classmethod(custom_queryset))
        self.get_list_view()

    def test_custom_context(self):
        def custom_context(self, request, context, **kwargs):
            context['testcontext'] = 'foo'
            return context
        setattr(TestModelCrud, 'custom_context', classmethod(custom_context))
        self.get_list_view()

    def test_custom_get_success_url(self):

        TestModelCrud.createupdate_forms = dict(
            create=TestModelForm,
            update=TestModelForm)

        self.client_login()
        self.assertEqual(TestModel.objects.count(), 0)

        response = self.client.post("/crud/tests/testmodels/create/", {"name": "Test text", "email": "sa@me.org"})
        test_models = list(TestModel.objects.all())
        self.assertEqual(len(test_models), 1)
        self.assertEqual(response.url, "/crud/tests/testmodels/%s/" % test_models[0].pk)
        self.assertEqual(response.status_code, 302)

        response = self.client.post("/crud/tests/testmodels/1/update/", data={"name": "new_name"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/crud/tests/testmodels/%s/" % test_models[0].pk)

    def test_custom_detail_context(self):
        def custom_detail_context(self, request, context, **kwargs):
            context['testcontext'] = 'foo'
            return context
        setattr(TestModelCrud, 'custom_detail_context', classmethod(custom_detail_context))
        obj = TestModel.objects.create(name='object1')
        self.get_detail_view(obj)

    def test_iniline_formset(self):
        TestModelCrud.inlineformset = TestChildInlineFormset
        self.get_list_view()

    def test_undertospace_filter(self):
        model = 'test_model'
        t = Template('{% load crudbuilder %}{{model|undertospaced}}')
        c = Context({"model": model})
        result = t.render(c)
        self.assertEqual(result, 'Test Model')

    def test_model_fields_filter(self):
        obj = TestModel.objects.create(name='object1')
        t = Template(
            "{% load crudbuilder %}"
            "{% for field in obj|get_model_fields %}"
            "{{ field.name}},"
            "{% endfor %}"
        )
        c = Context({"obj": obj})
        result = t.render(c)
        self.assertEqual(result, 'id,name,email,created_at,')

    def test_get_value_filter(self):
        obj = TestModel.objects.create(name='object1')
        t = Template(
            "{% load crudbuilder %}"
            "{{obj|get_value:'name'}}"
        )
        c = Context({"obj": obj})
        result = t.render(c)
        self.assertEqual(result, 'object1')
