FROM python:3.12.9-bullseye

SHELL ["/bin/sh", "-c"]

COPY . /opt/chapiana/
WORKDIR /opt/chapiana/

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONFAULTHANDLER 1 \
    PYTHONUNBUFFERED 1 \
    PATH=/usr/local/nginx/bin:$PATH \
    DJANGO_ENV=production \
    DJANGO_SETTINGS_MODULE=config.production \
    DJANGO_CONFIGURATION=Production

RUN pip install --quiet --no-cache-dir pip==23.2.1 \
    apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./LICENSE LICENSE
COPY ./requirements/
RUN pip install --no-cache-dir -r requirements/$REQUIREMENTS.txt

EXPOSE 8000

VOLUME ["/opt/chapiana"]

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/postgres.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt update && apt -y install postgresql-client-16 && rm -rf /var/lib/apt/lists/*

COPY ..

COPY ./opt/entrypoint.sh /
RUN chmod 755 /opt/entrypoint
ENTRYPOINT ["sh", "/opt/chapiana/entrypoint.sh" ]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:$PORT"]

# Run gunicorn as the default command
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "config.wsgi:application"]
