from django import forms
from .models import Email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('__all__')