"""Simple in-memory moderation utilities."""

from datetime import datetime

REPORT_QUEUE = []
AUDIT_LOG = []


def log_action(user, action, target):
    AUDIT_LOG.append(
        {
            "timestamp": datetime.utcnow(),
            "user": getattr(user, "username", "anonymous"),
            "action": action,
            "target": target,
        }
    )


def queue_report(user, target):
    entry = {
        "timestamp": datetime.utcnow(),
        "user": getattr(user, "username", "anonymous"),
        "target": target,
    }
    REPORT_QUEUE.append(entry)
    log_action(user, "report", target)
