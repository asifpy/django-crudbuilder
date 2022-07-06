import django_tables2 as tables
from django_tables2.utils import A

from crudbuilder.abstract import BaseBuilder
from crudbuilder.helpers import (
    model_class_form,
    plural,
    custom_postfix_url
)


class TableBuilder(BaseBuilder):
    """
    Table builder which returns django_tables2 instance
    app : app name
    model : model name for which table will be generated
    table_fields : display fields for tables2 class
    css_table : css class for generated tables2 class
    """
    def generate_table(self):
        model_class = self.get_model_class().__class__

        detail_url_name = '{}-{}-detail'.format(
            self.app, custom_postfix_url(self.crud(), self.model)
        )

        main_attrs = dict(
            pk=tables.LinkColumn(detail_url_name, args=[A('pk')])
        )

        meta_attrs = dict(
            model=model_class,
            fields=('pk',) + self.tables2_fields if self.tables2_fields else ('pk',),
            attrs={
                "class": self.tables2_css_class,
                "empty_text": "No {} exist".format(plural(self.model))
            })

        main_attrs['Meta'] = type('Meta', (), meta_attrs)
        klass = type(
            model_class_form(self.model + 'Table'),
            (tables.Table,),
            main_attrs
        )
        return klass
