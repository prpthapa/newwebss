"""
Public-facing views for the Notes site.

Includes:
- The four page views (index, subject, chapter, topic).
- Two API endpoints (contact, note-view increment).
- Backward-compatible subject shortcuts (/physics/, /chemistry/, /computer-science/).

Security notes:
- `contact_submit` is rate-limited (django-ratelimit) to mitigate spam/abuse.
  The frontend posts the CSRF token in `X-CSRFToken`; the @csrf_protect-by-
  default policy applies.
- `increment_note_view` is rate-limited to prevent trivial view-count inflation.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Chapter, ContactMessage, Note, Subject, Topic

# Reuse the application logger configured in settings.LOGGING.
logger = logging.getLogger("notes.views")


# ---------------------------------------------------------------------------
# Page views
# ---------------------------------------------------------------------------
def index(request):
    subjects = Subject.objects.filter(is_active=True).prefetch_related("chapters")
    return render(request, "index.html", {"subjects": subjects})


def subject_detail(request, slug):
    """Subject detail page showing all chapters."""
    subject = get_object_or_404(Subject, slug=slug, is_active=True)
    chapters = subject.chapters.filter(is_active=True).prefetch_related("topics")
    return render(
        request,
        "subject_detail.html",
        {"subject": subject, "chapters": chapters},
    )


def chapter_detail(request, subject_slug, chapter_slug):
    """Chapter detail page showing all topics."""
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    chapter = get_object_or_404(
        Chapter,
        slug=chapter_slug,
        subject=subject,
        is_active=True,
    )
    topics = chapter.topics.filter(is_active=True).prefetch_related("notes")
    return render(
        request,
        "chapter_detail.html",
        {"subject": subject, "chapter": chapter, "topics": topics},
    )


def topic_detail(request, subject_slug, chapter_slug, topic_slug):
    """Topic detail page showing all notes/images."""
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    chapter = get_object_or_404(
        Chapter,
        slug=chapter_slug,
        subject=subject,
        is_active=True,
    )
    topic = get_object_or_404(
        Topic,
        slug=topic_slug,
        chapter=chapter,
        is_active=True,
    )
    notes = topic.notes.filter(is_active=True).order_by("page_number")
    return render(
        request,
        "topic_detail.html",
        {"subject": subject, "chapter": chapter, "topic": topic, "notes": notes},
    )


# ---------------------------------------------------------------------------
# Backward-compatible subject shortcuts (/physics/, /chemistry/, /computer-science/)
# ---------------------------------------------------------------------------
def _render_subject_shortcut(request, slug: str):
    """Render a subject_detail page for the given slug, falling back to index."""
    try:
        subject = Subject.objects.get(slug=slug, is_active=True)
    except Subject.DoesNotExist:
        return render(
            request,
            "index.html",
            {"subjects": Subject.objects.filter(is_active=True)},
        )
    chapters = subject.chapters.filter(is_active=True).prefetch_related("notes")
    return render(
        request,
        "subject_detail.html",
        {"subject": subject, "chapters": chapters},
    )


def physics(request):
    return _render_subject_shortcut(request, "physics")


def chemistry(request):
    return _render_subject_shortcut(request, "chemistry")


def computer_science(request):
    return _render_subject_shortcut(request, "computer-science")


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------
# django-ratelimit is optional in code but pinned in requirements.txt.
try:
    from django_ratelimit.decorators import ratelimit
except ImportError:  # pragma: no cover - requirement pinning handles this
    ratelimit = None

if ratelimit is None:
    logger.warning(
        "django-ratelimit is NOT installed; rate limits on contact and view "
        "counters are INACTIVE."
    )


@require_POST
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def contact_submit(request):
    """
    Handle contact form submission via AJAX.

    The view relies on Django's CSRF middleware — the front-end sends the
    token in `X-CSRFToken` (see `static/script.js`).
    """
    form = ContactForm(request.POST)
    if not form.is_valid():
        # Return the first human-readable error message back to the client.
        first_field, errors = next(iter(form.errors.items()))
        msg = (
            f"{first_field}: {errors[0]}"
            if first_field != "__all__"
            else errors[0]
        )
        logger.info("Contact form rejected: %s", msg)
        return JsonResponse(
            {"success": False, "message": msg, "errors": form.errors},
            status=400,
        )

    data = form.cleaned_data
    ContactMessage.objects.create(
        name=data["name"],
        email=data["email"],
        subject=data["subject"],
        message=data["message"],
    )

    # Best-effort notification. Failures are logged but never block the user.
    try:
        body = (
            f"New contact form submission:\n\n"
            f"Name: {data['name']}\n"
            f"Email: {data['email']}\n"
            f"Subject: {data['subject']}\n\n"
            f"Message:\n{data['message']}"
        )
        send_mail(
            subject=f"New Contact: {data['subject']}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
    except Exception:  # noqa: BLE001
        logger.warning(
            "Failed to send contact-form notification email.", exc_info=True
        )

    logger.info("Contact form accepted from %s", data["email"])
    return JsonResponse(
        {
            "success": True,
            "message": "Thank you for your message! We will get back to you soon.",
        }
    )


@require_POST
@ratelimit(key="ip", rate="60/m", method="POST", block=True)
def increment_note_view(request, note_id):
    """Increment view count for a note. Rate-limited per IP."""
    note = get_object_or_404(Note, id=note_id, is_active=True)
    note.increment_views()
    return JsonResponse({"success": True, "views": note.views})