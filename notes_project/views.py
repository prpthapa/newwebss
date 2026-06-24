"""
Project-level views.

`notes/views.py` holds the public-facing page views and API endpoints for the
Notes app; this module owns only what's project-wide:

- /healthz/ lives in `health.py` (no DB access).
- The 404/500 handlers referenced by the project's `urls.py` so a
  production stack trace never leaks to end users.
- The legal pages linked from the public footer (privacy, terms).
"""
from django.shortcuts import render


def page_not_found(request, exception=None):
    """Custom 404 page — referenced as handler404 in urls.py."""
    return render(request, "404.html", status=404)


def server_error(request):
    """Custom 500 page — referenced as handler500 in urls.py."""
    return render(request, "500.html", status=500)


def privacy_policy(request):
    """Stub privacy policy. Operators should replace this with real copy."""
    return render(request, "privacy_policy.html")


def terms_of_service(request):
    """Stub terms of service. Operators should replace this with real copy."""
    return render(request, "terms.html")