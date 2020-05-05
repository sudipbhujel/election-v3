from django import forms

from election.models import ElectionForm
from django.forms.models import fields_for_model, model_to_dict
from accounts.models import User


class ElectionFillForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = ElectionForm
        exclude = ('voter', )
        fields = '__all__'