from django import forms


class SelectTemplateForm(forms.Form):
    template = forms.CharField(label="template", max_length=100)
