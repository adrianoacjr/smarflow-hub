from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from presentation.dependencies.di_whatsapp import di_whatsapp

from infrastructure.gateways.message_gateway_whatsapp import MessageGatewayWhatsapp

router = APIRouter()

@router.get("/whatsapp/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub, challenge")

    from os import getenv
    VERIFY_TOKEN = getenv("WHATSAPP_VERIFY_TOKEN", "change-me")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return JSONResponse(content=int(challenge))
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("whatsapp/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    raw_body = await request.body()
    headers = request.headers
    gateway: MessageGatewayWhatsapp = di_whatsapp.get_gateway()

    signature = headers.get("x-hub-signature-256")
    if not gateway.verify_webhook_signatures(raw_body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    payload = await request.json()

    background_tasks.add_task(process_incoming_payload, payload)
    return {"status": "received"}

def process_incoming_payload(payload: dict):
    entries = payload.get("entry", [])
    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            value = change.get("value", [])
            messages = value.get("messages", [])
            statuses = value.get("statuses", [])

            for m in messages:
                from application.message.receive_message import ReceiveMessage
                try:
                    phone = m["from"]
                    text = m.get("text", {}).get("body", "")
                except Exception as e:
                    print("process_incoming_payload error:", e)

            for s in statuses:
                pass
