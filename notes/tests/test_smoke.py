"""
Smoke tests for the public site + studio gate.

These are intentionally minimal — they don't aim for coverage, they aim to
catch the obvious regressions a future contributor might introduce:

- /healthz/ returns 200 with no DB access.
- /  renders the index page.
- /subject/<bad-slug>/ 404s.
- /api/contact/ accepts a valid CSRF-protected POST and rejects one without
  the token.
- /studio/ redirects unauthenticated requests to the login page; the
  configured credentials log in successfully.
"""
from django.test import TestCase, override_settings
from django.urls import reverse

from ..models import Subject


class HealthCheckTests(TestCase):
    def test_healthz(self):
        response = self.client.get("/healthz/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class PublicPageTests(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_subject_detail_404(self):
        response = self.client.get(
            reverse("subject_detail", kwargs={"slug": "no-such-subject"})
        )
        self.assertEqual(response.status_code, 404)

    def test_404_uses_custom_template(self):
        response = self.client.get("/no-such-url/")
        self.assertEqual(response.status_code, 404)
        # The custom 404 template extends base.html, so the page loader div
        # (an element unique to base.html) should be present.
        self.assertIn(b'id="pageLoader"', response.content)


class ContactSubmitTests(TestCase):
    def _post(self, data, *, with_csrf=True):
        # Always use a CSRF-enforcing client. With `with_csrf=True` we
        # also fetch a valid token from a priming GET. With `with_csrf=False`
        # we deliberately omit the header so Django's CSRF middleware
        # rejects the request.
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        if with_csrf:
            csrf_token = client.get("/").cookies["csrftoken"].value
            return client.post(
                "/api/contact/", data, HTTP_X_CSRFTOKEN=csrf_token
            )
        return client.post("/api/contact/", data)

    def test_contact_submit_without_csrf_is_rejected(self):
        response = self._post(
            {
                "name": "Alice",
                "email": "alice@example.com",
                "subject": "Hello",
                "message": "This is a test message.",
            },
            with_csrf=False,
        )
        self.assertEqual(response.status_code, 403)

    def test_contact_submit_with_csrf_succeeds(self):
        response = self._post(
            {
                "name": "Alice",
                "email": "alice@example.com",
                "subject": "Hello",
                "message": "This is a test message.",
            },
            with_csrf=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    def test_contact_submit_validates_email(self):
        response = self._post(
            {
                "name": "Alice",
                "email": "not-an-email",
                "subject": "Hello",
                "message": "This is a test message.",
            },
            with_csrf=True,
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])


@override_settings(
    STUDIO_USERNAME="tester",
    STUDIO_PASSWORD="s3cret-test-pw",
)
class StudioAuthTests(TestCase):
    def test_dashboard_redirects_unauthed(self):
        response = self.client.get(reverse("studio:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("studio:login"), response["Location"])

    def test_login_with_correct_creds(self):
        response = self.client.post(
            reverse("studio:login"),
            {"username": "tester", "password": "s3cret-test-pw"},
        )
        self.assertEqual(response.status_code, 302)
        # Follow the redirect to confirm the session was set.
        self.client.session.save()
        self.assertIn("studio_authed", self.client.session)
        self.assertTrue(self.client.session["studio_authed"])

    def test_login_with_wrong_creds(self):
        response = self.client.post(
            reverse("studio:login"),
            {"username": "tester", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        # The login template shows the error inline; assert it's there.
        self.assertContains(response, "Invalid username or password.")