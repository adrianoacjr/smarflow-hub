from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos.whatsapp_webhook_dto import WhatsAppWebhookDTO
from application.use_cases.integration.receive_whatsapp_message import ReceiveWhatsAppMessage

from infrastructure.dependencies.di_message import di_message

from core.database import get_session

router = APIRouter()

@router.post("/whatsapp-webhook", status_code=status.HTTP_200_OK)
async def whatsapp_webhook(payload: WhatsAppWebhookDTO, session: AsyncSession = Depends(get_session)):
    service: ReceiveWhatsAppMessage = di_message.get_receive_whatsapp_message(session)

    await service.execute(
        user_id=1,
        customer_id=1,
        content=payload.content
    )

    return {"status": "received"}
