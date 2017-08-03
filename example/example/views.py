from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from crudbuilder.views import ViewBuilder
from example.crud import PersonCrud

builder = ViewBuilder('example', 'person', PersonCrud)
builder.generate_crud()

PersonListView = builder.classes['PersonListView']
PersonCreateView = builder.classes['PersonCreateView']
PersonUpdateView = builder.classes['PersonUpdateView']
PersonDetailView = builder.classes['PersonDetailView']


class MyCustomPersonListView(PersonListView):
    def get_context_data(self, **kwargs):
        context = super(MyCustomPersonListView, self).get_context_data(**kwargs)
        context['your_template_variable'] = 'Your new template variable'
        return context

    def get_queryset(self):
        # return super(MyCustomPersonListView, self).get_queryset()
        return self.model.objects.none()


class MyCustomPersonDetailView(PersonDetailView):
    def get_context_data(self, **kwargs):
        context = super(MyCustomPersonDetailView, self).get_context_data(**kwargs)
        # context['form'] = YourAnotherForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # form = YourAnotherForm(request.POST)
        # if form.is_valid():
            # Do your custom logic here
        #    pass
        return HttpResponseRedirect(
            reverse(
                'person-detail',
                args=[self.object.pk]
            )
        )


class MyCustomPersonCreateView(PersonCreateView):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        # # your custom logic goes here
        return HttpResponseRedirect(reverse('mycustom-people'))
