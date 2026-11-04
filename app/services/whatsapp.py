import requests
from flask import current_app
import logging
from app.utils.message_policy import validate_outbound_text
from app.utils.phone import normalize_recipient

logger = logging.getLogger(__name__)

class WhatsAppService:

    def __init__(self):
        self.token = current_app.config.get("WHATSAPP_TOKEN")
        self.phone_number_id = current_app.config.get(
            "WHATSAPP_PHONE_NUMBER_ID"
        )

        if not self.token or not self.phone_number_id:
            raise ValueError(
                "WhatsApp configuration missing"
            )

        self.session = requests.Session()

        self.url = (
            f"https://graph.facebook.com/v21.0/"
            f"{self.phone_number_id}/messages"
        )

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_message(
        self,
        recipient_number,
        message_text
    ):
        recipient_number = normalize_recipient(recipient_number)
        message_text = validate_outbound_text(message_text)
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message_text
            }
        }

        try:
            response = self.session.post(
                self.url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            logger.info(
                "Message accepted by WhatsApp API"
            )

            return {
                "success": True,
                "data": response.json()
            }

        except requests.exceptions.RequestException as e:

            error_message = str(e)

            if getattr(e, "response", None):
                error_message = f'Provider returned HTTP {e.response.status_code}'

            logger.error(
                f"WhatsApp API Error: {error_message}"
            )

            return {
                "success": False,
                "error": error_message
            }
