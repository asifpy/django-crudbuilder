from django import forms
from crudbuilder.tests.models import TestModel


class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print(self.request.user)
        super(TestModelForm, self).__init__(*args, **kwargs)
