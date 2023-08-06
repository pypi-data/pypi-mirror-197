from __future__ import annotations
from celery import shared_task
from django.conf import settings
from network_service_client.client import (
    Client as NetworkClient,
    Network as NetworkDTO,
    NetworksNames,
)
from credential.register_credentials_factory.models import FactoryArgsModel
from credential.register_credentials_factory.factory import Creator
from organizations.models import Organization, OrganizationDID, Issuer
from credential.models import Credential, CredentialBlockChainRegister


@shared_task
def register_credential_by_network_task(credential_id: int, net: str) -> str:
    credential: Credential = Credential.objects.get(id=credential_id)
    organization: Organization = credential.organization
    organization_did: OrganizationDID | None = OrganizationDID.objects.filter(
        organization=organization, network_name=NetworksNames[net]
    ).first()
    issuer: Issuer = Issuer.objects.filter(organization=organization).first()
    is_registered: CredentialBlockChainRegister | None = CredentialBlockChainRegister.objects.filter(credential=credential).first()
    if is_registered:
        return f"The credential {credential_id} has already been registered in network {net} the register record id is {is_registered.id}."
    if not organization_did:
        raise Exception(
            f"You cannot register an vc without DID as an issuer, organization: {organization.id} network: {NetworksNames[net]}"
        )
    if not issuer:
        raise Exception(
            f"Your organization is not an issuer you cannot register an vc, organization: {organization.id} network: {NetworksNames[net]}"
        )
    if not issuer.active:
        raise Exception(
            f"Your organization issuer status is not active you cannot register an vc, organization: {organization.id} network: {NetworksNames[net]}"
        )
    register: CredentialBlockChainRegister = CredentialBlockChainRegister(
        credential=credential,
        status="PENDING",
        network=net,
    )
    register.save()
    network_data: NetworkDTO = NetworkClient(
        service_host=settings.NETWORK_SERVICE_HOST
    ).get_network_by_name(NetworksNames[net])
    props = FactoryArgsModel(net=network_data)
    context = Creator().create_object(props).request()
    tx_hash: str = context.register_credential(
        organization.keys.address,
        organization.keys.private_key,
        organization_did.did,
        credential.credential,
        credential.credential_type.name,
    )
    register.status = "SUCCESS"
    register.tx_hash = tx_hash
    register.save()

    return tx_hash
