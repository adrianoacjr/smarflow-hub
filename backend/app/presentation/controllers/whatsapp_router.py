from presentation.dtos.whatsapp_message_dto import whatsappMessageRequest, whatsappMessageResponse
from application.whatsapp.send_whatsapp_message import SendWhatsappMessage
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.post("/whatsapp/send", response_model=whatsappMessageResponse)
async def send_whatsapp_message(
    request: whatsappMessageRequest,
    send_whatsapp_message_use_case: SendWhatsappMessage = Depends()
):
    try:
        success = send_whatsapp_message_use_case.execute(
            phone_number=request.phone_number,
            content=request.content
        )
        return whatsappMessageResponse(success=success, content=request.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
