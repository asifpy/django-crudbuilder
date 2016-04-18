from django.dispatch import Signal

# post save signals for single model instance
post_create_signal = Signal(providing_args=['request', 'instance'])
post_update_signal = Signal(providing_args=['request', 'instance'])

# post save signals for inline formset
post_inline_create_signal = Signal(providing_args=['request', 'parent', 'children'])
post_inline_update_signal = Signal(providing_args=['request', 'parent', 'children'])


crudbuilder_signals = {
    'inlineformset': {
        'create': post_inline_create_signal,
        'update': post_inline_update_signal
    },
    'instance': {
        'create': post_create_signal,
        'update': post_update_signal
    }
}
