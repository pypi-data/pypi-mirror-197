from django import forms
from credential.models import Credential


class CredentialBaseForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ("credential_type", "subject_did",)
