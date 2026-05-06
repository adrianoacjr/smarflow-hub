from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.dtos.whatsapp_webhook_dto import WhatsAppWebhookDTO
from infrastructure.database import get_session
from infrastructure.dependencies.di_message import get_received_message
from infrastructure.dependencies.di_ai import get_analyze_message

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.get("/whatsapp-webhook", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok"}

@router.get("/whatsapp-webhook", status_code=status.HTTP_200_OK)
async def receive_whatsapp(
    payload: WhatsAppWebhookDTO,
    session: AsyncSession = Depends(get_session),
):
    message = await get_received_message(session).execute(
        phone=payload.phone,
        content=payload.content,
    )

    reply = await get_analyze_message(session).execute(
        customer_id=message.customer_id,
        inbound_content=payload.content,
    )

    return {"status": "received", "reply": reply.content}
