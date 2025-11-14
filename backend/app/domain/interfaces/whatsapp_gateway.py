from domain.models.message import Message
from abc import ABC, abstractmethod
from typing import Protocol

class IWhatsappGateway(ABC):
    @abstractmethod
    def send_whatsapp_message(self, to_number: str, content: str) -> bool:
        pass
