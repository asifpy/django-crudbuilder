from django.contrib.contenttypes.models import ContentType
import django_tables2 as tables
from django_tables2.utils import A

from crudbuilder.text import model_class_form, plural

class TableBuilder(object):
	def __init__(self, app, model, table_fields=None, css_table=None):
		self.app = app
		self.model = model
		self.table_fields = table_fields
		self.css_table = css_table

	def get_model_class(self):
		c = ContentType.objects.get(app_label=self.app, model=self.model)
		return c.model_class()

	def generate_table(self):
		model_class = self.get_model_class()
		detail_url_name = '{}-{}-detail'.format(self.app, self.model)

		main_attrs = dict(
			id = tables.LinkColumn(detail_url_name, args=[A('pk')])
			)
		meta_attrs = dict(
			model=model_class,
			fields=('id',) + self.table_fields if self.table_fields else ('id',),
			attrs={
				"class": "table table-bordered table-condensed",
				"empty_text" : "No {} exist".format(plural(self.model))
        	})

		main_attrs['Meta'] = type('Meta', (), meta_attrs)
		klass = type(model_class_form(self.model + 'Table'), (tables.Table,), main_attrs)
		return klass
