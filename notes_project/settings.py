"""
Django settings for the Notes project.

Hardened for production. See the project README for the env-var contract.
"""
import os
from pathlib import Path

import dj_database_url
from decouple import Csv, config
from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Secrets & environment
# ---------------------------------------------------------------------------
# A list of placeholder values that must never be accepted as a real secret.
# If a real placeholder is committed, the app refuses to start so it can't
# boot with a known public key.
_SECRET_PLACEHOLDERS = {
    "",
    "change-me-in-production",
    "change-me",
    "your-secret-key-here",
    "changeme",
    "secret",
    "django-insecure",  # django-admin startproject default
}


def _require_secret(var_name: str) -> str:
    """Read an env var and refuse to start if it is missing or a known placeholder."""
    value = config(var_name, default="")
    if value in _SECRET_PLACEHOLDERS:
        raise ImproperlyConfigured(
            f"{var_name} is missing or set to a placeholder value. "
            f"Set a real value in the environment (e.g. via Render's env-var UI)."
        )
    return value


SECRET_KEY = _require_secret("SECRET_KEY")

# `cast=bool` is required — `default='False'` would otherwise be a truthy string.
DEBUG = config("DEBUG", default="False", cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=Csv(),
)

# CSRF_TRUSTED_ORIGINS must include the https:// origins the front-end POSTs
# to. Pull it from the env (comma-separated) and fall back to https:// versions
# of every ALLOWED_HOSTS entry so the contact form works out of the box.
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=",".join(f"https://{h}" for h in ALLOWED_HOSTS),
    cast=Csv(),
)

# Studio credentials (env-based, kept as-is for backward compatibility).
STUDIO_USERNAME = _require_secret("STUDIO_USERNAME")
STUDIO_PASSWORD = _require_secret("STUDIO_PASSWORD")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "notes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "notes_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "notes_project.wsgi.application"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# `dj-database-url` parses DATABASE_URL on Heroku/Render-style platforms.
DATABASES = {
    "default": dj_database_url.config(
        default=config(
            "DATABASE_URL",
            default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        ),
        conn_max_age=600,
    )
}

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Locale
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ---------------------------------------------------------------------------
# Cache (used by django-ratelimit and the studio-auth lockout)
# ---------------------------------------------------------------------------
# If the operator provides CACHE_URL (e.g. redis://...) use it; otherwise the
# in-process LocMem cache is fine for a single-worker dev server. Render runs
# multiple gunicorn workers, so the lockout is best-effort there — that's an
# acceptable trade-off for a non-public studio endpoint.
# `dj-database-url` parses DATABASE_URL on Heroku/Render-style platforms.
# Cache is set up separately below — django-ratelimit and the studio-auth
# lockout both need a working cache.
CACHES = {
    "default": {
        # Default to in-process LocMemCache. On Render (multi-worker) the
        # studio lockout is per-process — that's an acceptable trade-off for
        # a non-public endpoint. For strict lockout, set CACHE_BACKEND to a
        # shared backend (e.g. django.core.cache.backends.redis.RedisCache)
        # and CACHE_LOCATION to the redis://... URL.
        "BACKEND": config(
            "CACHE_BACKEND",
            default="django.core.cache.backends.locmem.LocMemCache",
        ),
        "LOCATION": config("CACHE_LOCATION", default="notes-cache"),
        "TIMEOUT": config("CACHE_TIMEOUT", default=300, cast=int),
    }
}


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
# By default we just print emails to stdout (and to the application log via
# Django's SMTP backend printing to the console). In production set
# EMAIL_BACKEND + standard SMTP vars (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
# EMAIL_HOST_PASSWORD, EMAIL_USE_TLS) in Render's env-var UI.
EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="Notes <noreply@tpradeep.com.np>",
)
# Honor standard SMTP knobs when the operator supplies them.
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
# Target inbox for contact-form notifications.
CONTACT_NOTIFICATION_EMAIL = config(
    "CONTACT_NOTIFICATION_EMAIL",
    default="pdpthapa1515@gmail.com",
)


# ---------------------------------------------------------------------------
# Security — applied only when DEBUG is False.
# ---------------------------------------------------------------------------
# Render's free tier sits behind a TLS-terminating proxy. We must trust the
# X-Forwarded-Proto header so request.is_secure() returns True and the
# SECURE_* cookies work.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"

if not DEBUG:
    # Cookies only over HTTPS.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

    # Force HTTPS. Render's load balancer handles the redirect, so this is a
    # belt-and-braces measure.
    SECURE_SSL_REDIRECT = True

    # HSTS — Render sets HSTS at the edge too, but apply it at the app layer
    # so non-Render deployments (Docker/VPS) get it for free.
    SECURE_HSTS_SECONDS = 31_536_000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Admin / studio session lifetime — short by default. The studio is
    # private, so a longer session is fine, but the admin should expire.
    SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", default=60 * 60 * 8, cast=int)
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
# Stream everything to stdout so Render's log drainer picks it up. No file
# handlers (they would die with the gunicorn worker anyway).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": config("LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "notes": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
