from django.contrib import admin
from credential.models import CredentialType, Credential, CredentialBlockChainRegister
from django.utils.translation import gettext_lazy as _
from credential.forms import CredentialBaseForm
import json
from organizations.models import Organization
from credential.tasks import register_credential_by_network_task


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

    def response_change(self, request, obj):
        if "_register-in-block-chain" in request.POST:
            for net in obj.organization.networks:
                register_credential_by_network_task.delay(obj.id, net)

        return super().response_change(request, obj)


class CredentialBlockChainRegisterAdmin(admin.ModelAdmin):
    model = CredentialBlockChainRegister
    readonly_fields = ["credential", "register_date", "status", "network", "tx_hash"]


admin.site.register(CredentialBlockChainRegister, CredentialBlockChainRegisterAdmin)
admin.site.register(CredentialType, CredentialTypeAdmin)
admin.site.register(Credential, CredentialAdmin)
