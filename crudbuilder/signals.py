from django.dispatch import Signal

# post save signals for single model instance
instance_signal = Signal(providing_args=['request', 'instance'])
post_create_signal = instance_signal
post_update_signal = instance_signal

# post save signals for inline formset
inline_signal = Signal(providing_args=['request', 'parent', 'children'])
post_inline_create_signal = inline_signal
post_inline_update_signal = inline_signal


signals = {
    'inlineformset': {
        'create': post_inline_create_signal,
        'update': post_inline_update_signal
    },
    'instance': {
        'create': post_create_signal,
        'update': post_update_signal
    }
}
