from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings

from crudbuilder.views import ViewBuilder
from crudbuilder.tests.crud import TestModelCrud
from crudbuilder.tests.forms import TestModelForm
from crudbuilder.tests.tables import TestModelTable


class ViewBuilderTestCase(TestCase):
    def setUp(self):
        self.builder = ViewBuilder('tests', 'testmodel', TestModelCrud)

    def test_get_model_class(self):
        model_class = self.builder.get_model_class
        self.assertEqual(model_class.__name__, "TestModel")

    def test_list_view(self):
        list_view = self.builder.generate_list_view()
        self.assertEqual(list_view.__name__, "TestmodelListView")
        self.assertEqual(list_view.table_pagination, self.builder.tables2_pagination)

    def test_create_view(self):
        create_view = self.builder.generate_create_view()
        self.assertEqual(create_view.__name__, 'TestmodelCreateView')

    def test_detail_view(self):
        detail_view = self.builder.generate_detail_view()
        self.assertEqual(detail_view.__name__, 'TestmodelDetailView')

    def test_update_view(self):
        update_view = self.builder.generate_update_view()
        self.assertEqual(update_view.__name__, 'TestmodelUpdateView')

    def test_table_pagination(self):
        tables2_pagination = self.builder.tables2_pagination
        self.assertEqual(tables2_pagination, 20)

        # test the default pagination
        self.builder.tables2_pagination = None
        list_view = self.builder.generate_list_view()
        self.assertEqual(list_view.table_pagination, 10)

    def test_tables2_feilds(self):
        tables2_feilds = self.builder.tables2_fields
        self.assertEqual(tables2_feilds,  ('name', 'email'))

    def test_custom_list_view_permission(self):
        # test custom permission
        self.builder.permission_required = dict(list='mycustom_list_perm')
        self.assertEqual(
            self.builder.view_permission('list'),
            'mycustom_list_perm')

    def test_default_list_view_permission(self):
        # test auto generated (default) permission
        self.assertEqual(
            self.builder.view_permission('list'),
            'tests.testmodel_list')

    def test_check_crud_views(self):
        self.builder.generate_crud()
        generated_views = [
            view_type for view_type in self.builder.classes.keys()]
        expected_views = [
            'TestmodelCreateView',
            'TestmodelListView',
            'TestmodelDetailView',
            'TestmodelUpdateView',
            'TestmodelDeleteView'
        ]
        self.assertEqual(sorted(generated_views), sorted(expected_views))


class ActualViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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
        response = self.client.get('/crud/tests/testmodels/')
        self.assertEqual(200, response.status_code)

    def test_user_not_logged_in(self):
        response = self.client.get('/crud/tests/testmodels/')
        self.assertEqual(302, response.status_code)

    def test_user_logged_in(self):
        self.get_list_view()

    def test_view_with_custom_form(self):
        TestModelCrud.custom_modelform = TestModelForm
        self.get_list_view()

    def test_view_with_custom_tables2(self):
        TestModelCrud.custom_table2 = TestModelTable
        self.get_list_view()

    def test_view_with_custom_template(self):
        template = 'custom.html'
        TestModelCrud.custom_templates = dict(list=template)
        self.get_list_view()














