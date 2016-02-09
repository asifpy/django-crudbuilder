import django_tables2 as tables
from crudbuilder.tests.models import TestModel


class TestModelTable(tables.Table):

    class Meta:
        model = TestModel
        fields = '__all__'
        attrs = {"class": "table table-bordered table-condensed"}
