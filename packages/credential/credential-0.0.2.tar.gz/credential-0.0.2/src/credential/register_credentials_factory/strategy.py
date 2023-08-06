from .abstractions import ANetworkStrategy
from alastria_service_client.client import (
    AClient as AlastriaAClinet,
    Client as AlastriaClient,
)
from .models import FactoryArgsModel
from network_service_client.enums import ContractsNames
from alastria_service_client.validators import (
    Address,
    NetworkValidator,
    SignatureValidator,
    RunRawTransaction,
    DelegateCallValidator,
    AddIssuerCredentialValidator,
    OnlyNetworkValidator,
)
from django.conf import settings
from alastria_identity.types import Credential as CreateCredential, JwtToken
from alastria_identity.services import (
    TokenService,
)


class AlastriaNetworkStrategy(ANetworkStrategy):
    def __init__(self, props: FactoryArgsModel):
        self.alastria_service_client: AlastriaAClinet = AlastriaClient(
            service_host=settings.ALASTRIA_SERVICE_HOST
        )
        self.props = props
        network_data = self.props.net
        self.network_body = NetworkValidator(
            provider=network_data.node["path"],
            identity_manager_contract_address=list(
                filter(
                    lambda contract: contract["name"]
                    == ContractsNames.AlastriaIdentityManager.value,
                    network_data.contracts,
                )
            )[0]["address"],
            identity_manager_contract_abi=list(
                filter(
                    lambda contract: contract["name"]
                    == ContractsNames.AlastriaIdentityManager.value,
                    network_data.contracts,
                )
            )[0]["abi"],
            public_key_registry_contract_address=list(
                filter(
                    lambda contract: contract["name"]
                    == ContractsNames.AlastriaPublicKeyRegistry.value,
                    network_data.contracts,
                )
            )[0]["address"],
            public_key_registry_contract_abi=list(
                filter(
                    lambda contract: contract["name"]
                    == ContractsNames.AlastriaPublicKeyRegistry.value,
                    network_data.contracts,
                )
            )[0]["abi"],
            credential_registry_contract_abi=list(
                filter(
                    lambda contract: contract["name"]
                    == ContractsNames.AlastriaCredentialRegistry.value,
                    network_data.contracts,
                )
            )[0]["abi"],
            credential_registry_contract_address=list(
                filter(
                    lambda contract: contract["name"]
                    == ContractsNames.AlastriaCredentialRegistry.value,
                    network_data.contracts,
                )
            )[0]["address"],
            chainId=network_data.chain_id,
        )

    def register_credential(
        self,
        issuer_address: str,
        issuer_private_key: str,
        issuer_did: str,
        credential: dict,
        credential_type: str,
    ) -> str:
        jwt = CreateCredential(
            iss="",
            context=[""],
            credential_subject={"name": credential},
            credential_type="",
        ).build_jwt()
        jwt_token = JwtToken(**jwt)
        sig_credential = TokenService(private_key=issuer_private_key).sign_jwt(
            jwt_token
        )
        transaction_hash = self.alastria_service_client.run_raw_transaction(
            RunRawTransaction(
                raw_transaction=self.alastria_service_client.signature(
                    SignatureValidator(
                        transaction=self.alastria_service_client.delegate_call(
                            DelegateCallValidator(
                                data=self.alastria_service_client.add_issuer_credential(
                                    AddIssuerCredentialValidator(
                                        did=issuer_did,
                                        network=self.network_body,
                                        sig_credential=sig_credential,
                                    )
                                ).response,
                                issuer_address=issuer_address,
                                network=self.network_body,
                                address_delegate_call=Address(
                                    self.network_body.credential_registry_contract_address
                                ),
                            ),
                        ).response,
                        private_key=issuer_private_key,
                        network=self.network_body,
                    )
                ).response,
                network=self.network_body,
            )
        ).response
        return transaction_hash


class LacchainNetworkStrategy(ANetworkStrategy):
    def __init__(self, props: FactoryArgsModel):
        self.props = props
        self.prefix = props.net.did_prefix

    def register_credential(
        self,
        issuer_address: str,
        issuer_private_key: str,
        issuer_did: str,
        credential: dict,
        credential_type: str,
    ) -> str:
        raise NotImplementedError()
