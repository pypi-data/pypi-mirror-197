from django.contrib import admin
from credential.models import CredentialType, Credential
from django.utils.translation import gettext_lazy as _
from credential.forms import CredentialBaseForm
import json
from organizations.models import Organization


class CredentialTypeAdmin(admin.ModelAdmin):
    model = CredentialType
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name", "schema")


class CredentialAdmin(admin.ModelAdmin):
    model = Credential
    form = CredentialBaseForm
    change_form_template = "admin/credential/change_form_credential.html"

    def save_model(self, request, obj, form, change):
        obj.credential = json.loads(request.POST.get("credential"))
        obj.created_by = request.user
        obj.organization = Organization.objects.filter(operators=request.user).first()
        super().save_model(request, obj, form, change)


admin.site.register(CredentialType, CredentialTypeAdmin)
admin.site.register(Credential, CredentialAdmin)
