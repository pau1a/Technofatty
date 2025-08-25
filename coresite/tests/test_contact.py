from unittest import mock

from django.urls import reverse
from django.test import TestCase
from django.core.cache import cache


class ContactViewTests(TestCase):
    def setUp(self):
        cache.clear()

    @mock.patch("coresite.views.contact_event")
    @mock.patch("coresite.views.ContactNotifier")
    def test_valid_post_redirects(self, mock_notifier, mock_log):
        data = {
            "name": "A",
            "email": "a@example.com",
            "subject": "Hello",
            "message": "Hi",
            "website": "",
        }
        response = self.client.post(reverse("contact"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/contact/?sent=1")
        expected = data.copy()
        expected.pop("website")
        mock_notifier.return_value.send.assert_called_once_with(**expected)
        mock_log.assert_called_once_with("submitted_success", mock.ANY)

    def test_invalid_post_rerenders_with_errors_and_focus(self):
        response = self.client.post(reverse("contact"), {})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(
            form.fields["name"].widget.attrs.get("autofocus"),
            "autofocus",
        )

    def test_sent_query_param_renders_success_banner(self):
        response = self.client.get("/contact/?sent=1")
        self.assertContains(response, "Your message has been sent.")

    def test_honeypot_field_triggers_validation_error(self):
        data = {
            "name": "A",
            "email": "a@example.com",
            "subject": "Hello",
            "message": "Hi",
            "website": "spam",
        }
        response = self.client.post(reverse("contact"), data)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("website", form.errors)

    @mock.patch("coresite.views.contact_event")
    @mock.patch("coresite.views.ContactNotifier")
    def test_throttled_post_skips_delivery(self, mock_notifier, mock_log):
        data = {
            "name": "A",
            "email": "a@example.com",
            "subject": "Hello",
            "message": "Hi",
            "website": "",
        }
        self.client.post(reverse("contact"), data, REMOTE_ADDR="1.1.1.1")
        mock_notifier.return_value.send.assert_called_once()
        mock_log.assert_called_once_with("submitted_success", mock.ANY)
        mock_notifier.return_value.send.reset_mock()
        mock_log.reset_mock()
        response = self.client.post(reverse("contact"), data, REMOTE_ADDR="1.1.1.1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/contact/?sent=1")
        mock_notifier.return_value.send.assert_not_called()
        mock_log.assert_called_once_with("throttle_hit", mock.ANY)
