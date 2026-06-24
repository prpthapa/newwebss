"""
Gunicorn configuration. Auto-loaded when gunicorn is started with no
extra flags (e.g. `gunicorn notes_project.wsgi:application`).

Render's PORT env var controls the bind address; on its free tier, the
service listens on 0.0.0.0:10000 by default, so we honor $PORT when set.
"""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Render sets WEB_CONCURRENCY in newer environments; fall back to 3 for
# the free web dyno (2 vCPU).
workers = int(os.environ.get("WEB_CONCURRENCY", "3"))
worker_class = "sync"

# Cold-start tolerance: free-tier services can take 30-60s to boot.
timeout = 120
graceful_timeout = 30
keepalive = 5

# Stream logs to stdout/stderr so Render's log drainer can pick them up.
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Preload the app so we don't pay the import cost per worker.
preload_app = True