"""
Studio auth: simple session-based gate for the private /studio/ section.

The studio uses a hardcoded username/password pair from .env (STUDIO_USERNAME,
STUDIO_PASSWORD) — this is intentionally separate from Django's auth system so
it does not interact with the admin or any user accounts. A successful login
sets ``request.session['studio_authed'] = True``; the decorator checks for it.
"""
from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods


SESSION_KEY = 'studio_authed'


def get_studio_creds():
    """Return the configured (username, password) tuple."""
    return settings.STUDIO_USERNAME, settings.STUDIO_PASSWORD


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


@require_http_methods(['POST'])
def do_studio_logout(request):
    """Clear the studio session key. Always redirects to the login page."""
    request.session.pop(SESSION_KEY, None)
    return redirect('studio:login')
