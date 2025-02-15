#!/bin/sh
set -e

python manage.py migrate --no-input
python manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python3 manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

gunicorn --bind :$PORT \
    src.wsgi --access-logfile - --error-logfile - --log-level info

echo "Done setting the configuration"