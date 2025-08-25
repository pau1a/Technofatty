import logging

logger = logging.getLogger(__name__)


class ContactNotifier:
    def send(self, name: str, email: str, message: str) -> None:
        logger.info({"event": "contact_message", "name": name, "email": email, "message": message})
