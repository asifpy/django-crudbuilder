import django_tables2 as tables
from crudbuilder.tests.models import TestModel


class TestModelTable(tables.Table):

    class Meta:
        model = TestModel
        attrs = {"class": "table table-bordered table-condensed"}
