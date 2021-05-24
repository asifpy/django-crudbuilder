import operator
import six
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings
from django.contrib import messages

from crudbuilder.signals import crudbuilder_signals

if six.PY3:
    from functools import reduce


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
        global_login_required = getattr(
            settings, 'LOGIN_REQUIRED_FOR_CRUD', False)

        if global_login_required or self.login_required:
            if not request.user.is_authenticated:
                return self.handle_login_required(request)

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permission.
    """
    def check_permissions(self, request):
        perms = self.permissions
        result = request.user.has_perm(perms) if perms else True
        return result

    def dispatch(self, request, *args, **kwargs):
        has_permission = self.check_permissions(request)
        global_permission_required = getattr(
            settings, 'PERMISSION_REQUIRED_FOR_CRUD', False)

        if global_permission_required or self.permission_required:
            if not has_permission:
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
        try:
            context['exclude'] = self.detailview_excludes
        except:
            context['exclude'] = None
        name = model._meta.verbose_name
        context['actual_model_name'] = name
        context['verbose_model_name'] = name
        name_plural = model._meta.verbose_name_plural
        context['pluralized_model_name'] = name_plural
        context['verbose_model_name_plural'] = name_plural
        context['custom_postfix_url'] = self.custom_postfix_url
        context['project_name'] = getattr(
            settings, 'PROJECT_NAME', 'CRUDBUILDER')
        return context

    @property
    def get_actual_signal(self):
        view = 'update' if self.object else 'create'
        if self.inlineformset:
            return crudbuilder_signals['inlineformset'][view]
        else:
            return crudbuilder_signals['instance'][view]


class BaseDetailViewMixin(CrudBuilderMixin):
    def get_context_data(self, **kwargs):
        context = super(BaseDetailViewMixin, self).get_context_data(**kwargs)
        context['inlineformset'] = self.inlineformset
        if self.custom_detail_context:
            custom_detail_context = self.custom_detail_context(self.request, context, **kwargs)
            context.update(custom_detail_context)
        return context


class CreateUpdateViewMixin(CrudBuilderMixin):
    """Common form_valid() method for both Create and Update views"""
    def get_form_kwargs(self):
        kwargs = super(CreateUpdateViewMixin, self).get_form_kwargs()
        if self.custom_form:
            kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        signal = self.get_actual_signal
        instance = form.save(commit=False)
        signal.send(sender=self.model, request=self.request, instance=instance)
        instance.save()
        form.save_m2m()
        return super(CreateUpdateViewMixin, self).form_valid(form)


class BaseListViewMixin(CrudBuilderMixin):
    """
    - Search implementation for tables2 in ListView.
    - search_fields will be defined in actual model
    - Override get_queryset method of ListView
    """
    def get_queryset(self):
        if self.custom_queryset:
            objects = self.custom_queryset(self.request, **self.kwargs)
        else:
            objects = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            q_list = [
                Q(
                    ('{}__icontains'.format(field), search))
                for field in self.crud.search_fields
            ]
            objects = objects.filter(reduce(operator.or_, q_list))
        return objects.order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super(BaseListViewMixin, self).get_context_data(**kwargs)
        if self.custom_context:
            custom_context = self.custom_context(self.request, context, **kwargs)
            context.update(custom_context)
        return context


class InlineFormsetViewMixin(CrudBuilderMixin):
    def get_context_data(self, **kwargs):
        context = super(
            InlineFormsetViewMixin, self).get_context_data(**kwargs)
        if self.request.POST:
            context['inlineformset'] = self.inlineformset(
                self.request.POST,
                instance=self.object
            )
        else:
            context['inlineformset'] = self.inlineformset(
                instance=self.object
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        inlineformset = context['inlineformset']

        if inlineformset.is_valid():
            parent = form.save(commit=False)
            inlineformset.instance = parent
            children = inlineformset.save(commit=False)

            # execute post signals
            signal = self.get_actual_signal
            signal.send(
                sender=self.model,
                request=self.request,
                parent=parent,
                children=children)

            parent.save()
            inlineformset.save()
            inlineformset.save_m2m()

            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(
                self.request, inlineformset.non_form_errors())
            return self.render_to_response(
                self.get_context_data(form=form, inlineformset=inlineformset)
            )
