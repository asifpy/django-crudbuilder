from django import forms
from crudbuilder.tests.models import TestModel


class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = '__all__'
