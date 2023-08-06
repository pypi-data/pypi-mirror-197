from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from organizations.models import Organization


class CredentialType(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    schema = models.JSONField(_("Schema"))

    def __str__(self):
        return self.name


class Credential(models.Model):
    credential_type = models.ForeignKey(CredentialType, on_delete=models.PROTECT)
    credential = models.JSONField(_("Credential"))
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    subject_did = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.credential_type.name}:{self.created_by.email}:{self.subject_did}"


class CredentialBlockChainRegister(models.Model):
    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)
    register_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200)
    network = models.CharField(max_length=200)
    tx_hash = models.TextField()
    
    def __str__(self):
        return f"{self.credential}:{self.status}:{self.network}"
