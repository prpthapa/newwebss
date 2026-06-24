"""
Studio auth: simple session-based gate for the private /studio/ section.

The studio uses a hardcoded username/password pair from .env (STUDIO_USERNAME,
STUDIO_PASSWORD) — this is intentionally separate from Django's auth system so
it does not interact with the admin or any user accounts. A successful login
sets ``request.session['studio_authed'] = True``; the decorator checks for it.

Hardening:
- Constant-time compare via ``hmac.compare_digest`` so we don't leak the
  expected password length via timing.
- A simple lockout backed by the Django cache: 5 failed attempts per IP in
  15 minutes blocks that IP for 1 hour. On multi-worker hosts (Render's free
  tier) the lockout is best-effort because each worker has its own cache;
  switch ``CACHE_BACKEND`` to a shared backend (Redis) for strict mode.
"""
import hmac
import logging
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger("notes.studio_auth")

SESSION_KEY = "studio_authed"

# Lockout configuration.
LOCKOUT_MAX_FAILS = 5
LOCKOUT_WINDOW_SECONDS = 15 * 60  # 15 minutes
LOCKOUT_DURATION_SECONDS = 60 * 60  # 1 hour


def get_studio_creds():
    """Return the configured (username, password) tuple."""
    return settings.STUDIO_USERNAME, settings.STUDIO_PASSWORD


# ---------------------------------------------------------------------------
# Lockout helpers (cache-backed)
# ---------------------------------------------------------------------------
def _client_ip(request) -> str:
    """Best-effort client IP. Honours X-Forwarded-For (Render sets it)."""
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def _fail_count_key(ip: str) -> str:
    return f"studio_login_fail:{ip}"


def _lockout_key(ip: str) -> str:
    return f"studio_login_lock:{ip}"


def _is_locked(ip: str) -> bool:
    return cache.get(_lockout_key(ip)) is True


def _record_failure(ip: str) -> int:
    """Increment the failure count for the IP. Returns the new count."""
    key = _fail_count_key(ip)
    try:
        # incr is atomic in caches that support it (Redis); otherwise fall back.
        new_count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, LOCKOUT_WINDOW_SECONDS)
        new_count = 1
    if new_count >= LOCKOUT_MAX_FAILS:
        cache.set(_lockout_key(ip), True, LOCKOUT_DURATION_SECONDS)
        logger.warning("Studio login locked for IP %s after %d failures.", ip, new_count)
    return new_count


def _clear_failures(ip: str) -> None:
    cache.delete(_fail_count_key(ip))
    cache.delete(_lockout_key(ip))


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------
def studio_login_required(view_func):
    """
    Decorator: require an authenticated studio session.
    Redirects unauthenticated requests to /studio/login/?next=<current path>.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.session.get(SESSION_KEY):
            return view_func(request, *args, **kwargs)
        next_url = request.get_full_path()
        login_url = f"{reverse('studio:login')}?next={next_url}"
        return redirect(login_url)

    return _wrapped


def _constant_time_eq(a: str, b: str) -> bool:
    """Constant-time string comparison. Returns False on type/length mismatch
    without leaking the length difference."""
    if not isinstance(a, str) or not isinstance(b, str):
        return False
    return hmac.compare_digest(a, b)


def check_studio_credentials(request, username: str, password: str) -> tuple[bool, str | None]:
    """
    Validate the supplied username/password against the configured pair.

    Returns ``(ok, error_message)``. Applies the lockout rules: a locked IP
    gets ``(False, lockout_message)`` regardless of credentials.

    Side-effects:
    - On success: clears any prior failures for this IP.
    - On failure: increments the failure count and may impose a lockout.
    """
    ip = _client_ip(request)

    if _is_locked(ip):
        logger.info("Studio login rejected (locked): IP %s", ip)
        return False, (
            "Too many failed attempts. Try again in about an hour, or "
            "contact the site owner if you believe this is a mistake."
        )

    expected_user, expected_pass = get_studio_creds()
    ok = _constant_time_eq(username, expected_user) and _constant_time_eq(
        password, expected_pass
    )

    if ok:
        _clear_failures(ip)
        return True, None

    new_count = _record_failure(ip)
    logger.info(
        "Studio login failure #%d from IP %s (username=%r)",
        new_count,
        ip,
        username,
    )
    # Same generic message whether the username or the password was wrong.
    return False, "Invalid username or password."


@require_http_methods(["POST"])
def do_studio_logout(request):
    """Clear the studio session key. Always redirects to the login page."""
    request.session.pop(SESSION_KEY, None)
    return redirect("studio:login")