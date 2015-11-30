import operator
from django.db.models import Q
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings

from crudbuilder.helpers import mixedToUnder, plural
from crudbuilder.signals import post_update_signal, post_create_signal


class LoginRequiredMixin(object):
    """
    View mixin which verifies that login required for the crud builder
    """
    login_url = settings.LOGIN_URL
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def handle_login_required(self, request):
        return redirect_to_login(
            request.get_full_path(),
            self.login_url,
            self.redirect_field_name)

    def dispatch(self, request, *args, **kwargs):
        login_required = getattr(settings, 'LOGIN_REQUIRED_FOR_CRUD', False)

        if login_required:
            if not request.user.is_authenticated():
                return self.handle_login_required(request)

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permission.
    """
    def check_permissions(self, request):
        perms = self.permission_required
        result = request.user.has_perm(perms) if perms else True
        return result

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.check_permissions(request)
        permission_required = getattr(
            settings, 'PERMISSION_REQUIRED_FOR_CRUD', False)

        if permission_required and not has_permission:
            return redirect_to_login(
                request.get_full_path(),
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME)

        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class CrudBuilderMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """
    - Mixin to provide additional context data for the templates
    - app_label : return app_label for CRUD model
    - actual_model_name : returns the actual model name (person -> person)
    - pluralized_model_name : return the pluralized_model_name
    (person -> people)
    """
    def get_context_data(self, **kwargs):
        context = super(CrudBuilderMixin, self).get_context_data(**kwargs)
        model = context['view'].model
        context['app_label'] = model._meta.app_label
        context['actual_model_name'] = model.__name__.lower()
        context['pluralized_model_name'] = plural(model.__name__.lower())
        return context


class CreateUpdateViewMixin(CrudBuilderMixin):
    """Common form_valid() method for both Create and Update views"""

    @property
    def get_actual_signal(self):
        if self.object:
            return post_update_signal
        else:
            return post_create_signal

    def form_valid(self, form):
        signal = self.get_actual_signal
        instance = form.save(commit=False)
        signal.send(sender=self.model, request=self.request, instance=instance)
        instance.save()
        return super(CreateUpdateViewMixin, self).form_valid(form)


class BaseListViewMixin(CrudBuilderMixin):
    """
    - Search implementation for tables2 in ListView.
    - search_feilds will be defined in actual model
    - Override get_queryset method of ListView
    """
    def get_queryset(self):
        objects = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            q_list = [
                Q(
                    ('{}__icontains'.format(field), search)
                    ) for field in self.crud.search_feilds
                ]
            objects = objects.filter(reduce(operator.or_, q_list))
        return objects.order_by('-id')
