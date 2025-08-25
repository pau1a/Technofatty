from unittest import mock

from django.urls import reverse
from django.test import TestCase


class ContactViewTests(TestCase):
    @mock.patch("coresite.views.log_newsletter_event")
    @mock.patch("coresite.views.ContactNotifier")
    def test_valid_post_redirects(self, mock_notifier, mock_log):
        data = {"name": "A", "email": "a@example.com", "message": "Hi"}
        response = self.client.post(reverse("contact"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/contact/?sent=1")
        mock_notifier.return_value.send.assert_called_once_with(**data)
        mock_log.assert_called_once_with(mock.ANY, "submitted_success")

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
