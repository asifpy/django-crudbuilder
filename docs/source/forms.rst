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

		def __init__(self, *args, **kwargs):
			self.request = kwargs.pop('request', None)
			super(PersonEmploymentForm, self).__init__(*args, **kwargs)

	# yourapp/crud.py
	class PersonEmploymentCrud(BaseCrudBuilder):
		model = PersonEmployment
		custom_modelform = PersonEmploymentForm

.. note::
	
	If you want to plug custom modelform, then make sure to override form's ``__init__`` to get `request` param as mentioned above.


Separate CREATE and UPDATE forms
--------------------------------

You can also define separate forms for CreateView and UpdateView.::

	# yourapp/forms.py
	class PersonEmployementCreateForm(forms.ModelForm):
		class Meta:
			model = PersonEmployment
			exclude = ('person', 'medical_allowance')

		def __init__(self, *args, **kwargs):
			self.request = kwargs.pop('request', None)
			super(PersonEmployementCreateForm, self).__init__(*args, **kwargs)

	class PersonEmployementUpdateForm(forms.ModelForm):
		class Meta:
			model = PersonEmployment
			exclude = ('salary', 'year')

		def __init__(self, *args, **kwargs):
			self.request = kwargs.pop('request', None)
			super(PersonEmployementUpdateForm, self).__init__(*args, **kwargs)

	# yourapp/crud.py
	class PersonEmploymentCrud(BaseCrudBuilder):
		model = PersonEmployment
		createupdate_forms = {
			'create': PersonEmployementCreateForm,
			'update': PersonEmployementUpdateForm
		}

You can check `forms`_.py of example project on Github.

.. _forms: https://github.com/asifpy/django-crudbuilder/blob/master/example/example/forms.py

.. note::
	
	If you want to plug custom modelform, then make sure to override form's ``__init__`` to get `request` param as mentioned above.


Inline Formset (Parent child relation)
--------------------------------------

The latest version of django-crudbuilder supports inline formset. You can define your own InlineFormset and give it to CRUD class.::

	# yourapp/crud.py
	from crudbuilder.formset import BaseInlineFormset

	class PersonEmploymentInlineFormset(BaseInlineFormset):
		inline_model = PersonEmployment
		parent_model = Person
		exclude = ['created_by', 'updated_by']
		#formset_class = YourBaseInlineFormset
		#child_form = ChildModelForm

	class PersonCrud(BaseCrudBuilder):
		model = Person
		search_fields = ['name']
		tables2_fields = ('name', 'email')		
		inlineformset = PersonEmploymentInlineFormset


You can check `crud`_.py of example project on Github.

.. _crud: https://github.com/asifpy/django-crudbuilder/blob/master/example/example/crud.py


You can set the following arguments for InlineFormset class.::

	extra = 3		--> default number of forms of Child model
	can_delete = True  	--> Delete check box for child instance
	formset_class = None  	--> Django BaseInlineFormset class to override the methods of InlineFormset (For example, if you want to override clean())
	child_form		--> Modelform for Child model
	inline_model = None   	--> Child Model
	parent_model = None   	--> Parent Model
	exclude = []          	--> Exclude fields for Inline Formset
	fields = None         	--> Fields to disaply in inline formset
	fk_name = None        	--> More than one foreign key for the same parent model, then specify this




