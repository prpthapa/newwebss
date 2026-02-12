"""
Create or reset superuser from env vars (for deploy without Shell).
Uses: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD.
- If no superuser exists: creates one.
- If superuser exists and password env is set: resets that user's password so you can log in.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or reset superuser from env vars (no Shell needed)."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_PASSWORD not set; set it in Render Environment and redeploy."
                )
            )
            return

        existing = User.objects.filter(is_superuser=True).first()
        if existing:
            existing.set_password(password)
            existing.save()
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{existing.username}' password updated. Log in with that username and your env password.")
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
