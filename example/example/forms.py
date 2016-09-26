from django import forms

from example.models import PersonEmployment


class PersonEmploymentForm(forms.ModelForm):
    class Meta:
        model = PersonEmployment
        fields = '__all__'
        # exclude = ('person',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print(self.request.user)
        super(PersonEmploymentForm, self).__init__(*args, **kwargs)


class PersonEmployementCreateForm(forms.ModelForm):
    class Meta:
        model = PersonEmployment
        exclude = ('person', 'medical_allowance')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print(self.request.user)
        super(PersonEmployementCreateForm, self).__init__(*args, **kwargs)


class PersonEmployementUpdateForm(forms.ModelForm):
    class Meta:
        model = PersonEmployment
        exclude = ('salary', 'year')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print(self.request.user)
        super(PersonEmployementUpdateForm, self).__init__(*args, **kwargs)
