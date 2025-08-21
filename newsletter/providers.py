import time
from enum import Enum
from typing import Protocol

from django.conf import settings
from django.db import IntegrityError

from .models import NewsletterLead


class Result(Enum):
    SUCCESS = "success"
    ALREADY = "already"
    NEEDS_CONFIRM = "needs_confirm"
    SERVER_BUSY = "server_busy"
    ERROR = "error"


class NewsletterProvider(Protocol):
    def subscribe(self, email: str) -> Result:
        ...


class StubProvider:
    """Store emails locally for development."""

    def __init__(self, ip: str = "", ua: str = "", source: str = "") -> None:
        self.ip = ip
        self.ua = ua
        self.source = source

    def subscribe(self, email: str) -> Result:
        try:
            NewsletterLead.objects.create(
                email=email, ip=self.ip, ua=self.ua, source=self.source
            )
            return Result.SUCCESS
        except IntegrityError:
            return Result.ALREADY
        except Exception:
            return Result.ERROR


def get_provider(ip: str = "", ua: str = "", source: str = "") -> NewsletterProvider:
    name = getattr(settings, "NEWSLETTER_PROVIDER", "stub")
    if name == "stub":
        return StubProvider(ip=ip, ua=ua, source=source)
    # Future providers would be added here
    return StubProvider(ip=ip, ua=ua, source=source)
