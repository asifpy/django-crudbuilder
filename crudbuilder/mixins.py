import operator
from django.db.models import Q

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

class BaseListViewMixin(CrudBuilderMixin):
	"""
	- Search implementation for tables2 in ListView.
	- search_feilds will be defined in actual model
	- Override get_queryset method of ListView
	"""
	def get_queryset(self):
		objects = self.model.objects.all()
		search = self.request.GET.get('search')
		if search:
			q_list = [
				Q(('{}__icontains'.format(field), search)
					) for field in self.model.search_feilds
				]
			objects = objects.filter(reduce(operator.or_, q_list))
		return objects.order_by('-id')
