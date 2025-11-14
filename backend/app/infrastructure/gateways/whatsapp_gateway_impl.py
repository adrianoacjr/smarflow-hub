import requests
from app.domain.interfaces.whatsapp_gateway import IWhatsappGateway

class WhatsappGatewayImpl(IWhatsappGateway):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def send_whatsapp_message(self, to_number: str, content: str) -> bool:
        payload = {
            "to": to_number,
            "message": content
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.status_code == 200
