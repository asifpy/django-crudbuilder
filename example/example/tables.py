import django_tables2 as tables
from django_tables2.utils import A

from .models import Person


class CustomPersonTable(tables.Table):
    name = tables.LinkColumn('example-people-detail', args=[A('pk')])
    selection = tables.CheckBoxColumn(accessor='pk')

    class Meta:
        model = Person
        attrs = {"class": "table table-bordered table-condensed"}
        fields = ('name', 'email', 'selection')
