#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create superuser from env if none exists (no Shell needed on free tier)
python manage.py create_superuser_if_missing

echo "Build completed successfully!"
