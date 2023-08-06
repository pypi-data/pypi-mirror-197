from abc import ABC, abstractmethod
from .models import FactoryArgsModel
from alastria_service_client.validators import Address


class ANetworkStrategy(ABC):
    @abstractmethod
    def register_credential(
        self,
        issuer_address: str,
        issuer_private_key: str,
        issuer_did: str,
        credential: dict,
        credential_type: str,
    ) -> str:
        """"""


class AContext(ABC):
    @abstractmethod
    def request(self) -> ANetworkStrategy:
        """"""


class AFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_object(props: FactoryArgsModel) -> AContext:
        """"""
