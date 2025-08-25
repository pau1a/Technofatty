import hashlib
from django.test import TestCase

from coresite.models import ContactEvent
from coresite.services.contact import contact_event


class ContactEventTests(TestCase):
    def test_persists_event_and_hashes_ip(self):
        contact_event("test", {"ip": "1.2.3.4", "foo": "bar"})
        self.assertEqual(ContactEvent.objects.count(), 1)
        event = ContactEvent.objects.get()
        self.assertEqual(event.event_type, "test")
        self.assertEqual(event.meta, {"foo": "bar"})
        expected_hash = hashlib.sha256(b"1.2.3.4").hexdigest()
        self.assertEqual(event.ip_hash, expected_hash)
