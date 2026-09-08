#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Automatically creates superuser if variables exist; skips silently if already created
python manage.py createsuperuser --noinput || true