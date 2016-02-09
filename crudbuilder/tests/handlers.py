from django.dispatch import receiver
from crudbuilder.signals import post_create_signal, post_update_signal

from crudbuilder.tests.models import TestModel


@receiver(post_create_signal, sender=TestModel)
def post_create_signal_handler(sender, **kwargs):
    pass


@receiver(post_update_signal, sender=TestModel)
def post_update_signal_handler(sender, **kwargs):
    pass
