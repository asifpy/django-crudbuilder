from django import forms

from example.models import PersonEmployment


class PersonEmploymentForm(forms.ModelForm):
    class Meta:
        model = PersonEmployment
        fields = '__all__'
        # exclude = ('person',)


class PersonEmployementCreateForm(forms.ModelForm):
    class Meta:
        model = PersonEmployment
        exclude = ('person', 'medical_allowance')


class PersonEmployementUpdateForm(forms.ModelForm):
    class Meta:
        model = PersonEmployment
        exclude = ('salary', 'year')
