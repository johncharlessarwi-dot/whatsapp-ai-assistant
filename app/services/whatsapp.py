import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.token = current_app.config['WHATSAPP_TOKEN']
        self.phone_number_id = current_app.config['WHATSAPP_PHONE_NUMBER_ID']
        self.url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def send_message(self, recipient_number, message_text):
        """
        Send a text message via WhatsApp Cloud API.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_number,
            "type": "text",
            "text": {"preview_url": False, "body": message_text}
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {recipient_number}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            if e.response:
                logger.error(f"Response: {e.response.text}")
            return None
