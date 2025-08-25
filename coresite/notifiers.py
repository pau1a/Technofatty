import logging
import os
from pathlib import Path

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class ContactNotifier:
    def _ensure_outbox(self) -> None:
        outbox = Path(settings.EMAIL_FILE_PATH)
        outbox.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(outbox, 0o700)

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
