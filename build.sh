#!/usr/bin/env bash
# Render build script.
# Note: `makemigrations` is intentionally NOT run here. Generate migrations
# locally, review them, commit them, then let Render only *apply* them via
# `migrate`. Running makemigrations on the server silently mutates the schema
# when local models drift from what's committed.
set -euo pipefail

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput