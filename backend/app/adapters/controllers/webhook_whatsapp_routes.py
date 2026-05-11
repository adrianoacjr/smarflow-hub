from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.dtos.whatsapp_webhook_dto import WhatsAppWebhookDTO
from application.dtos.message.analyze_message_command import AnalyzeMessageCommand
from application.dtos.message.receive_message_command import ReceiveMessageCommand
from infrastructure.config import settings
from infrastructure.database import get_session
from infrastructure.dependencies.di_message import get_received_message
from infrastructure.dependencies.di_ai import get_analyze_message

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.get("/whatsapp", status_code=status.HTTP_200_OK)
async def verify_whatsapp_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    if hub_mode != "subscribe" or hub_verify_token != settings.WHATSAPP_VERIFY_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid verify token")
    return int(hub_challenge)

@router.get("/whatsapp", status_code=status.HTTP_200_OK)
async def receive_whatsapp(
    payload: WhatsAppWebhookDTO,
    session: AsyncSession = Depends(get_session),
):
    inbound = await get_received_message(session).execute(
        ReceiveMessageCommand(
            user_id=payload.user_id,
            source=payload.source,
            source_customer_ref=payload.phone,
            customer_name=payload.customer_name,
            content=payload.content,
            attachments=payload.attachments or [],
            automated=False,
        )
    )

    result = await get_analyze_message(session).execute(
        AnalyzeMessageCommand(inbound_message_id=inbound.id)
    )

    return {"status": "received", "outcome": result.outcome.value}
