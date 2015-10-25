'''
# GENERATE CRUD CLASSES
------------------------

>>> from crudbuilder.views import ViewBuilder
>>> builder = ViewBuilder('example', 'person')
>>> builder.generate_crud()
>>> builder.classes
{'PersonCreateView': <class 'django.views.generic.edit.PersonCreateView'>,
 'PersonDeleteView': <class 'crudbuilder.views.PersonDeleteView'>,
 'PersonListView': <class 'crudbuilder.views.PersonListView'>, 
 'PersonUpdateView': <class 'django.views.generic.edit.PersonUpdateView'>,
 'PersonDetailView': <class 'crudbuilder.views.PersonDetailView'>
}


# OVERRIDE AUTO GENERATED VIEWS
------------------------------

>>> from crudbuilder.views import ViewBuilder
>>> builder = ViewBuilder('example', 'person')
>>> builder.generate_crud()

>>> PersonListView = builder.classes['PersonListView']
>>> class CustomPersonListView(PersonListView):
>>>		def get_context_data(self, **kwargs):
>>>			context = super(CustomPersonListView, self).get_context_data(**kwargs)
>>>			context['your_template_variable'] = 'Your new template variable'
>>>			return context

>>> PersonCreateView = builder.classes['PersonCreateView']
>>> class CustomPersonCreateView(PersonCreateView):
>>>		def form_valid(self, form):
>>>			object = form.save(commit=False)
>>>			object.user = self.request.user
>>>			return HttpResponseRedirect(reverse('url-name'))

# OVERRIDE AUTO GENERATED TABLE (from django_tables2)
-----------------------------------------------------

>>> from crudbuilder.tables import TableBuilder
>>> builder = TableBuilder('example', 'person')
>>> PersonTable = builder.generate_table()
>>> class CustomPersonTable(PersonTable):
>>>		# add your custom implementation here
'''