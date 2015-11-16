from django.dispatch import receiver
from crudbuilder.signals import post_create_signal, post_update_signal

from example.models import Person


@receiver(post_create_signal, sender=Person)
def post_create_signal_handler(sender, **kwargs):
    # print "execute after create action"
    request = kwargs['request']
    instance = kwargs['instance']

    instance.created_by = request.user
    instance.save()


@receiver(post_update_signal, sender=Person)
def post_update_signal_handler(sender, **kwargs):
    # print "execute after update action"
    request = kwargs['request']
    instance = kwargs['instance']

    instance.updated_by = request.user
    instance.save()

