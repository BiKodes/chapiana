FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip

COPY ./requirements.txt /app/
RUN pip install -r ./requirements.txt

COPY . /app/

COPY ./scripts/start.sh /app/
RUN sed -i 's/\r$//' ./scripts/start.sh && \
    chmod +x ./scripts/start.sh

ENTRYPOINT [ "sh", "./scripts/start.sh" ]
