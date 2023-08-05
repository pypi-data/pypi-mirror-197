from django_jsonform.forms.fields import JSONFormField
from django import forms
from credential.models import Credential


def builder(schema: dict) -> forms.ModelForm:
    class DinamicForm(forms.Form):
        credential = JSONFormField(schema=schema)

    return DinamicForm
