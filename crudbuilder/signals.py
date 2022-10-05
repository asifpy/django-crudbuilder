from django.dispatch import Signal

# post save signals for single model instance
post_create_signal = Signal()
post_update_signal = Signal()

# post save signals for inline formset
post_inline_create_signal = Signal()
post_inline_update_signal = Signal()


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
