#!/bin/sh

set -e
set -x

python manage.py migrate --no-input
python manage.py collectstatic --no-input

daphne core.asgi:application -b 0.0.0.0
