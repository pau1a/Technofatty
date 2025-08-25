import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class ContactNotifier:
    def send(self, name: str, email: str, subject: str, message: str) -> None:
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
