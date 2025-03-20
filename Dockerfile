FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends postgresql libpq-dev build-essential
RUN pip install poetry
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /nexus

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

COPY app/ .
