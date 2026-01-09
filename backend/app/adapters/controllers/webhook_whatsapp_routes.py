from fastapi import APIRouter, status

from application.dtos.whatsapp_webhook_dto import WhatsAppWebhookDTO
from application.use_cases.integration.receive_whatsapp_message import ReceiveWhatsAppMessage

def build_webhook_whatsapp_router(
    receive_whatsapp_message: ReceiveWhatsAppMessage,
) -> APIRouter:
    router = APIRouter()

    @router.post("/whatsapp-webhook", status_code=status.HTTP_200_OK)
    async def whatsapp_webhook(payload: WhatsAppWebhookDTO):
        await receive_whatsapp_message.execute(
            user_id=1,
            customer_id=1,
            content=payload.content
        )

        return {"status": "received"}

    return router
