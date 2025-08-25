import re
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from django.test import TestCase


class AccountWorkflowTests(TestCase):
    def _signup(self, username="alice", email="alice@example.com", password="StrongPass123"):
        response = self.client.post(
            reverse("signup"),
            {
                "username": username,
                "email": email,
                "password1": password,
                "password2": password,
            },
        )
        return response

    def test_signup_sends_activation_email(self):
        self._signup()
        user = User.objects.get(username="alice")
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Activate your account", email.subject)
        self.assertIn("/activate/", email.body)

    def test_activation_activates_user(self):
        self._signup()
        email = mail.outbox[0]
        match = re.search(r"/activate/([^/]+)/([^/]+)/", email.body)
        self.assertIsNotNone(match)
        uidb64, token = match.groups()
        user = User.objects.get(username="alice")
        self.assertFalse(user.is_active)
        response = self.client.get(reverse("activate", kwargs={"uidb64": uidb64, "token": token}))
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_login_and_logout_flow(self):
        User.objects.create_user(username="bob", email="bob@example.com", password="Secret123")
        response = self.client.post(reverse("account_login"), {"username": "bob", "password": "Secret123"})
        self.assertRedirects(response, reverse("account"))
        self.assertEqual(self.client.get(reverse("account")).status_code, 200)
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
        response = self.client.get(reverse("account"))
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('account')}")

    def test_password_reset_flow(self):
        User.objects.create_user(username="carol", email="carol@example.com", password="OldPass123")
        response = self.client.post(reverse("password_reset"), {"email": "carol@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("reset", email.subject.lower())
        match = re.search(r"/account/reset/([^/]+)/([^/]+)/", email.body)
        self.assertIsNotNone(match)
        uidb64, token = match.groups()
        reset_confirm = reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
        response = self.client.post(
            reset_confirm,
            {"new_password1": "NewPass456", "new_password2": "NewPass456"},
        )
        self.assertRedirects(response, reverse("password_reset_complete"))
        self.assertTrue(self.client.login(username="carol", password="NewPass456"))

    def test_account_home_requires_login(self):
        response = self.client.get(reverse("account"))
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('account')}")
