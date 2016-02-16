Forms
=====

If NO custom forms defined in CRUD class, then by default crudbuilder will generate modelform from Django modelform factory.

Custom Modelform in CRUD class
------------------------------

You can define your own custom modelform in yourapp/forms.py and the same will be used for CRUD class. As shown below::

	# yourapp/forms.py
	class PersonEmploymentForm(forms.ModelForm):
		class Meta:
			model = PersonEmployment
			fields = '__all__'
			# exclude = ('person',)

	# yourapp/crud.py
	class PersonEmploymentCrud(BaseCrudBuilder):
		model = PersonEmployment
		custom_modelform = PersonEmploymentForm


Separate CREATE and UPDATE forms
--------------------------------

You can also define separate forms for CreateView and UpdateView.::

	# yourapp/forms.py
	class PersonEmployementCreateForm(forms.ModelForm):
		class Meta:
			model = PersonEmployment
			exclude = ('person', 'medical_allowance')

	class PersonEmployementUpdateForm(forms.ModelForm):
		class Meta:
			model = PersonEmployment
			exclude = ('salary', 'year')

	# youapp/crud.py
	class PersonEmploymentCrud(BaseCrudBuilder):
		model = PersonEmployment
		createupdate_forms = {
			'create': PersonEmployementCreateForm,
			'update': PersonEmployementUpdateForm
		}

You can check `forms`_.py of example project on Github.


.. _forms: https://github.com/asifpy/django-crudbuilder/tree/master/crudbuilder/templates







