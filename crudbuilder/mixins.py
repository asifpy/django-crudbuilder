from crudbuilder.text import mixedToUnder, plural

class CrudBuilderMixin(object):
	"""
	- Mixin to provide additional context data for the templates
	- app_label : return app_label for CRUD model
	- actual_model_name : returns the actual model name (person -> person)
	- pluralized_model_name : return the pluralized_model_name (person -> people)
	"""
	
	def get_context_data(self, **kwargs):
		context = super(CrudBuilderMixin, self).get_context_data(**kwargs)
		model = context['view'].model
		context['app_label'] = model._meta.app_label
		context['actual_model_name'] = mixedToUnder(model.__name__)
		context['pluralized_model_name'] = plural(model.__name__.lower())
		return context