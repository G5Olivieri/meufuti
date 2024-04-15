FROM python:3.11-alpine

RUN apk add -U --no-cache \
    build-base \
    libpq-dev

RUN pip install --upgrade pip && pip install pipenv