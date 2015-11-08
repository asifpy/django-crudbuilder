import operator
from django.db.models import Q
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings

from crudbuilder.text import mixedToUnder, plural


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
        if settings.LOGIN_REQUIRED_FOR_CRUD:
            if not request.user.is_authenticated():
                return self.handle_login_required(request)

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class CrudBuilderMixin(LoginRequiredMixin):
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
        context['actual_model_name'] = mixedToUnder(model.__name__)
        context['pluralized_model_name'] = plural(model.__name__.lower())
        return context


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
                    ) for field in self.model.search_feilds
                ]
            objects = objects.filter(reduce(operator.or_, q_list))
        return objects.order_by('-id')
