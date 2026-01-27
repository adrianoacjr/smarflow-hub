from fastapi import APIRouter, status

from adapters.dtos.whatsapp_webhook_dto import WhatsAppWebhookDTO
from application.use_cases.integration.receive_whatsapp_message import ReceiveWhatsAppMessage
from application.use_cases.integration.process_ai_reply import ProcessAIReply

def build_webhook_whatsapp_router(
    receive_whatsapp_message: ReceiveWhatsAppMessage,
    process_ai_reply: ProcessAIReply,
) -> APIRouter:
    router = APIRouter()

    @router.get("/whatsapp-webhook", status_code=status.HTTP_200_OK)
    async def whatsapp_webhook_health():
        return {"status": "ok"}

    @router.post("/whatsapp-webhook", status_code=status.HTTP_200_OK)
    async def whatsapp_webhook(payload: WhatsAppWebhookDTO):
        await receive_whatsapp_message.execute(
            user_id=1,
            customer_id=1,
            content=payload.content
        )

        ai_response = await process_ai_reply.execute(
            customer_id=1,
            inbound_content=payload.content,
        )

        return {"status": "received", "reply": ai_response.content}

    return router
