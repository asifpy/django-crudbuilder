from django import forms

from example.models import PersonEmployment


class PersonEmploymentForm(forms.ModelForm):
    class Meta:
        model = PersonEmployment
        fields = '__all__'
        #exclude = ('person',)