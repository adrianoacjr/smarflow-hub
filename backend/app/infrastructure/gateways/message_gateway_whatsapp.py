import os
import requests
import hmac, hashlib
from typing import Optional

from domain.interfaces.whatsapp_gateway import IWhatsappGateway

class MessageGatewayWhatsapp(IWhatsappGateway):
    def __init__(self, api_url: str = None, token: str = None, app_secret: str = None):
        self.api_url = api_url or os.getenv("WHATSAPP_API_URL")
        self.token = token or os.getenv("WHATSAPP_TOKEN")
        self.app_secret = app_secret or os.getenv("WHATSAPP_APP_SECRET")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def send_whatsapp_message(self, to_number: str, content: str, template_name: Optional[str] = None, metadata: Optional[dict] = None) -> bool:
        payload = {}
        if template_name:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "en_US"},
                }
            }
        else:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "text",
                "text": {"body": content}
            }

        try:
            resp = requests.post(self.api_url, json=payload, headers=self._headers(), timeout=15)
            resp.raise_for_status()
            return True
        except requests.HTTPError as e:
            print("WhatsApp send error:", e, getattr(e.response, "text", ""))
            return False
        except Exception as e:
            print("Whatsapp send exception:", str(e))
            return False
        
    def verify_webhook_signatures(self, raw_body: bytes, header_signature: str) -> bool:
        if not self.app_secret:
            return True
        if not header_signature:
            return False
        sha_name, signature = header_signature.split("=", 1)
        if sha_name != "sha256":
            return False
        mac = hmac.new(self.app_secret.encode(), msg=raw_body, digestmod=hashlib.sha256)
        expected = mac.hexdigest()
        return hmac.compare_digest(expected, signature)
