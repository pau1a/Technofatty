import stat
import tempfile
from pathlib import Path
from unittest import mock

from django.test import TestCase, override_settings

from coresite.notifiers import ContactNotifier


class ContactNotifierTests(TestCase):
    def test_sends_mail_with_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            outbox = Path(tmp) / "outbox"
            with override_settings(
                CONTACT_FROM_EMAIL="from@example.com",
                CONTACT_TO_EMAIL="to@example.com",
                EMAIL_FILE_PATH=outbox,
            ):
                with mock.patch("django.core.mail.send_mail") as mock_send:
                    ContactNotifier().send(
                        "Alice", "alice@example.com", "Hello", "Hi there"
                    )
                    mock_send.assert_called_once_with(
                        "Hello",
                        "From: Alice <alice@example.com>\n\nHi there",
                        "from@example.com",
                        ["to@example.com"],
                        reply_to=["alice@example.com"],
                    )

    def test_creates_outbox_with_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            outbox = Path(tmp) / "outbox"
            with override_settings(EMAIL_FILE_PATH=outbox):
                with mock.patch("django.core.mail.send_mail"):
                    ContactNotifier().send(
                        "Bob", "bob@example.com", "Hey", "Hello"
                    )
            self.assertTrue(outbox.exists())
            mode = stat.S_IMODE(outbox.stat().st_mode)
            self.assertEqual(mode, 0o700)
