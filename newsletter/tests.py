from unittest import mock

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import NewsletterSubscribeForm
from .providers import Result, StubProvider


class NewsletterFormTests(TestCase):
    def test_valid_email_passes(self):
        form = NewsletterSubscribeForm({"email": "test@example.com"})
        self.assertTrue(form.is_valid())

    def test_blank_shows_required_email(self):
        form = NewsletterSubscribeForm({"email": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("Please enter your email address to subscribe.", form.errors["email"][0])

    def test_malformed_shows_invalid_email(self):
        form = NewsletterSubscribeForm({"email": "notanemail"})
        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid email address", form.errors["email"][0])

    def test_honeypot_rejected_silently(self):
        form = NewsletterSubscribeForm({"email": "test@example.com", "website": "spam"})
        self.assertFalse(form.is_valid())
        self.assertNotIn("email", form.errors)


class NewsletterAdapterTests(TestCase):
    def test_stub_returns_already_on_duplicate(self):
        provider = StubProvider()
        self.assertEqual(provider.subscribe("dup@example.com"), Result.SUCCESS)
        self.assertEqual(provider.subscribe("dup@example.com"), Result.ALREADY)

class NewsletterViewTests(TestCase):
    def test_get_renders_form_noindex(self):
        response = self.client.get(reverse("newsletter_form"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Robots-Tag"], "noindex")
        self.assertContains(response, "Subscribe to the Newsletter")

    def test_single_opt_in_success(self):
        response = self.client.post(reverse("newsletter_form"), {"email": "a@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Thanks — you’re subscribed", response.content.decode())
        self.assertEqual(response["X-Robots-Tag"], "noindex")

    @override_settings(OPT_IN_MODE="double")
    def test_double_opt_in_success(self):
        response = self.client.post(reverse("newsletter_form"), {"email": "b@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("please check your inbox", response.content.decode())

    def test_duplicate_treated_as_success(self):
        self.client.post(reverse("newsletter_form"), {"email": "c@example.com"})
        response = self.client.post(reverse("newsletter_form"), {"email": "c@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Thanks", response.content.decode())

    def test_provider_timeout_maps_server_busy(self):
        with mock.patch("newsletter.providers.StubProvider.subscribe", side_effect=TimeoutError):
            response = self.client.post(reverse("newsletter_form"), {"email": "d@example.com"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("We’re having trouble right now", response.content.decode())

    def test_unknown_exception_maps_error(self):
        with mock.patch("newsletter.providers.StubProvider.subscribe", side_effect=Exception):
            response = self.client.post(reverse("newsletter_form"), {"email": "e@example.com"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("Something went wrong", response.content.decode())

    def test_rate_limit_ip(self):
        with override_settings(NEWSLETTER_RATE_LIMITS={"ip_per_hour": 1, "email_per_hour": 5}):
            self.client.post(reverse("newsletter_form"), {"email": "f@example.com"})
            response = self.client.post(reverse("newsletter_form"), {"email": "g@example.com"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("We’re having trouble right now", response.content.decode())

    def test_rate_limit_email(self):
        with override_settings(NEWSLETTER_RATE_LIMITS={"ip_per_hour": 5, "email_per_hour": 1}):
            self.client.post(reverse("newsletter_form"), {"email": "h@example.com"})
            response = self.client.post(reverse("newsletter_form"), {"email": "h@example.com"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("We’re having trouble right now", response.content.decode())
