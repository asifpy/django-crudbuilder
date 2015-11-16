from django.dispatch import Signal

post_create_signal = Signal(providing_args=['request', 'instance'])
post_update_signal = Signal(providing_args=['request', 'instance'])
