from typing import Optional

from domain.interfaces.whatsapp_gateway import IWhatsappGateway
from domain.models.message import Message
from datetime import datetime, timezone

class SendWhatsappMessage:
    def __init__(self, gateway: IWhatsappGateway):
        self.gateway = gateway

    def execute(self, user_id: int, customer_phone: str, content: str, template_name: Optional[str] = None, metadata: Optional[dict] = None) -> bool:
        msg = Message(
            user_id=user_id,
            customer_id=0,
            content=content,
            direction="outbound",
            source="whatsapp",
            timestamp=datetime.now(timezone.utc),
            automated=False,
            status="sent"
        )

        success = self.gateway.send_whatsapp_message(
            to_number=customer_phone,
            content=content,
            template_name=template_name,
            metadata=metadata or {}
        )

        return success
