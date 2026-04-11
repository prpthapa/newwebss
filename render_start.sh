#!/usr/bin/env bash
set -o pipefail

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
gunicorn notes_project.wsgi:application --bind "0.0.0.0:$PORT"
