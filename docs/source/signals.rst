Signals
=======

django-crudbuilder comes with two built-in signals to perform/execute specific actions after post create and post update views.
You can able to access ``request`` and ``instance`` in your own handlers.


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

Usage of these signals you can view in `handlers of example project`_ on Github.

.. _handlers of example project: https://github.com/asifpy/django-crudbuilder/blob/master/example/example/handlers.py