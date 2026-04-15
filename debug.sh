#!/bin/bash
set -e

echo "Checking Python..."
python --version

echo "Checking Django..."
python -c "import django; print('Django:', django.get_version())"

echo "Checking settings..."
python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings'); import django; django.setup(); print('Settings loaded')"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
gunicorn _core.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
