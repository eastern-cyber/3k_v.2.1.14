
web: python manage.py migrate --noinput && gunicorn _core.wsgi:application --bind 0.0.0.0:$PORT --workers 4
