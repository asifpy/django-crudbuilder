from django.test import TestCase

from crudbuilder.views import ViewBuilder
from crudbuilder.tests.crud import TestModelCrud


class ViewBuilderTestCase(TestCase):
    def setUp(self):
        self.builder = ViewBuilder('tests', 'testmodel', TestModelCrud)

    def test_get_model_class(self):
        model_class = self.builder.get_model_class
        self.assertEqual(model_class.__name__, "TestModel")

    def test_list_view(self):
        list_view = self.builder.generate_list_view()
        self.assertEqual(list_view.__name__, "TestmodelListView")
        self.assertEqual(list_view.table_pagination, {'per_page': self.builder.tables2_pagination})

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
        self.assertEqual(list_view.table_pagination, {'per_page': 10})

    def test_tables2_fields(self):
        tables2_fields = self.builder.tables2_fields
        self.assertEqual(tables2_fields,  ('name', 'email'))

    def test_custom_list_view_permission(self):
        # test custom permission
        self.builder.permissions = dict(list='mycustom_list_perm')
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
