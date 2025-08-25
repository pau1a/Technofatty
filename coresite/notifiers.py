import logging
import os

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class ContactNotifier:
    def _ensure_outbox(self) -> None:
        try:
            os.makedirs(settings.EMAIL_FILE_PATH, exist_ok=True)
        except Exception:
            pass

    def send(self, name: str, email: str, subject: str, message: str) -> None:
        self._ensure_outbox()
        send_mail(
            subject,
            f"From: {name} <{email}>\n\n{message}",
            settings.CONTACT_FROM_EMAIL,
            [settings.CONTACT_TO_EMAIL],
            reply_to=[email],
        )
        logger.info(
            {
                "event": "contact_message",
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
            }
        )
