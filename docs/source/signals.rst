Signals
=======

django-crudbuilder comes with built-in signals to perform/execute specific actions after post create and post update views.
You can able to access ``request`` and ``instance`` in your own handlers.

Usage of these signals you can view in `handlers of example project`_ on Github.

Following are the list of supported signals.::
	
	post_create_signal         --> runs after modelform.save() in CreateView
	post_update_signal         --> runs after modelform.save() in UpdateView
	post_inline_create_signal  --> runs after inlineformset.save() in CreateView
	post_inline_update_signal  --> runs after inlineformset.save() in UpdateView


post_create_signal
------------------

This signal will loaded/executed soon after the object gets created for specific model. In otherwords this will fires right after the ``modelform.save()`` method gets called during the CreateView.::
	
	# tutorial/handlers.py
	from django.dispatch import receiver
	from crudbuilder.signals import post_create_signal

	from example.models import Person

	@receiver(post_create_signal, sender=Person)
	def post_create_signal_handler(sender, **kwargs):
	    # print "execute after create action"
	    request = kwargs['request']
	    instance = kwargs['instance']

	    instance.created_by = request.user
	    instance.save()


post_update_signal
------------------

This signal will loaded/executed soon after the object gets updated for specific model. In otherwords this will fires right after the ``modelform.save()`` method gets called during the UpdateView.::
	
	# tutorial/handlers.py
	from django.dispatch import receiver
	from crudbuilder.signals import post_update_signal

	from example.models import Person

	@receiver(post_update_signal, sender=Person)
	def post_update_signal_handler(sender, **kwargs):
	    # print "execute after update action"
	    request = kwargs['request']
	    instance = kwargs['instance']

	    instance.updated_by = request.user
	    instance.save()


post_inline_create_signal
-------------------------

This signal will get executed soon after the inline formset gets saved which means this get fires right after the ``inlineformset.save()`` method gets called in CreateView.::

	# tutorial/handlers.py
	from django.dispatch import receiver
	from crudbuilder.signals import post_inline_create_signal

	@receiver(post_inline_create_signal, sender=Person)
	def post_inline_create_handler(sender, **kwargs):
		request = kwargs['request']
		parent = kwargs['parent']
		children = kwargs['children']

		parent.created_by = request.user
		parent.save()

		for child in children:
			child.created_by = request.user
			child.save()


post_inline_update_signal
-------------------------

This signal will get executed soon after the inline formset gets updated which means this get fires right after the ``inlineformset.save()`` method gets called in UpdateView.::

	# tutorial/handlers.py
	from django.dispatch import receiver
	from crudbuilder.signals import post_inline_update_signal

	@receiver(post_inline_update_signal, sender=Person)
	def post_inline_update_handler(sender, **kwargs):
		request = kwargs['request']
		parent = kwargs['parent']
		children = kwargs['children']

		parent.updated_by = request.user
		parent.save()

		for child in children:
			child.updated_by = request.user
			child.save()




.. _handlers of example project: https://github.com/asifpy/django-crudbuilder/blob/master/example/example/handlers.py