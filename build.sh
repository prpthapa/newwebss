#!/usr/bin/env bash
# Render build script — invoked by `render.yaml`.
# Idempotent: safe to re-run on every deploy.
set -euo pipefail

# 1. Install Python deps.
pip install --upgrade pip
pip install -r requirements.txt

# 2. Collect static files for WhiteNoise to serve.
python manage.py collectstatic --noinput

# 3. Apply database migrations.
python manage.py migrate --noinput