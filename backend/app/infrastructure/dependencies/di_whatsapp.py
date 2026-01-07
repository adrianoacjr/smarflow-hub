import os

from backend.app.infrastructure.gateways.whatsapp_message_gateway_whatsapp import MessageGatewayWhatsapp

from application.whatsapp.send_whatsapp_message import SendWhatsappMessage

class DIWhatsapp:
    def __init__(self):
        api_url = os.getenv("WHATSAPP_API_URL")
        token = os.getenv("WHATSAPP_TOKEN")
        app_secret = os.getenv("WHATSAPP_APP_SECRET")
        self._gateway = MessageGatewayWhatsapp(
            api_url=api_url,
            token=token,
            app_secret=app_secret
        )

    def get_gateway(self) -> MessageGatewayWhatsapp:
        return self._gateway
    
    def get_send_whatsapp_usecase(self) -> SendWhatsappMessage:
        return SendWhatsappMessage(self._gateway)
    
di_whatsapp = DIWhatsapp()
