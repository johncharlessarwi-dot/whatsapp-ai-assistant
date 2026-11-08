import requests
from flask import current_app
import logging
from app.utils.message_policy import validate_outbound_text
from app.utils.phone import normalize_recipient
from app.utils.graph_config import validate_phone_number_id

logger = logging.getLogger(__name__)

class WhatsAppService:

    def __init__(self):
        self.token = current_app.config.get("WHATSAPP_TOKEN")
        raw_phone_number_id = current_app.config.get(
            "WHATSAPP_PHONE_NUMBER_ID"
        )

        if not self.token or not raw_phone_number_id:
            raise ValueError(
                "WhatsApp configuration missing"
            )

        self.phone_number_id = validate_phone_number_id(raw_phone_number_id)
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

        except requests.exceptions.RequestException as exc:
            # Do not log or return exception URLs/headers; they can contain credentials.
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            if status_code is not None:
                logger.error("WhatsApp API request failed with HTTP %s", status_code)
            else:
                logger.error("WhatsApp API transport request failed")
            return {
                "success": False,
                "error": "WhatsApp provider request failed"
            }
