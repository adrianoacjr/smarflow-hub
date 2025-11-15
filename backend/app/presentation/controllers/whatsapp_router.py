from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks

from presentation.dtos.whatsapp_message_dto import whatsappMessageRequest, whatsappMessageResponse
from presentation.dependencies.di_whatsapp import di_whatsapp

router = APIRouter()

def get_send_uc():
    return di_whatsapp.get_send_whatsapp_usecase()

@router.post("/whatsapp/send", response_model=whatsappMessageResponse)
async def send_whatsapp_message(request: whatsappMessageRequest, background_tasks: BackgroundTasks, send_uc = Depends(get_send_uc)):
    background_tasks.add_task(send_uc.execute, 1, request.phone_number, request.content)
    return whatsappMessageResponse(success=True, content=request.content)
