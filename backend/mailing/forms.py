from django import forms
from .models import TemplateModel


class SelectTemplateForm(forms.Form):
    template = forms.ModelChoiceField(queryset=TemplateModel.objects.all())
