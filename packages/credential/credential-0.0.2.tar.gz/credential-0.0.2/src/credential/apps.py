from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CredentialConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "credential"
    verbose_name = _("Credential")
