"""
Production media file serving.

WhiteNoise handles static files; user uploads live under MEDIA_ROOT and must
be served separately when DEBUG is False. Render's free tier has an ephemeral
filesystem, so uploads survive only until the next deploy — use an external
object store (S3, Cloudinary, etc.) for durable media in production.
"""
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET


@require_GET
def serve_media(request, path: str):
    """Serve a file from MEDIA_ROOT with path-traversal protection."""
    media_root = Path(settings.MEDIA_ROOT).resolve()
    file_path = (media_root / path).resolve()

    # Reject paths that escape MEDIA_ROOT (e.g. ../../etc/passwd).
    try:
        file_path.relative_to(media_root)
    except ValueError as exc:
        raise Http404("Media file not found.") from exc

    if not file_path.is_file():
        raise Http404("Media file not found.")

    return FileResponse(
        file_path.open("rb"),
        as_attachment=False,
        filename=file_path.name,
    )
