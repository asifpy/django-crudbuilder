
class BaseBuilder(object):
	def __init__(self,
		app,
		model,
		form_excludes=None,
		custom_form=None,
		table_fields=None,
		css_table_class=None,
		custom_table=None,
		table_pagination=10):

		self.model = model
		self.app = app
		self.form_excludes = form_excludes
		self.custom_form = custom_form
		self.table_fields = table_fields
		self.css_table_class = css_table_class
		self.custom_table = custom_table
		self.table_pagination = table_pagination

