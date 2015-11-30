from django.test import TestCase
from crudbuilder.tests.crud import TestModelCrud

from crudbuilder.views import ViewBuilder


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






