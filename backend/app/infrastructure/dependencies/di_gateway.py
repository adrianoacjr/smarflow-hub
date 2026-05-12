from functools import lru_cache

from application.interfaces.message_gateway import IMessageGateway
from infrastructure.config import settings
from infrastructure.gateways.message_gateway_whatsapp import WhatsAppGateway

@lru_cache(maxsize=1)
def get_whatsapp_gateway() -> IMessageGateway:
    return WhatsAppGateway(
        token=settings.WHATSAPP_TOKEN,
        phone_number_id=settings.WHATSAPP_PHONE_NUMBER_ID,
    )
