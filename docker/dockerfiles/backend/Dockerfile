FROM python:3.12.0-slim-buster as base

ARG UID=1000
ARG GUID=1000

WORKDIR /backend

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR off
ENV POETRY_VIRTUALENVS_CREATE false

FROM base as builder
RUN apt-get update && apt-get install -y \
    --no-install-recommends build-essential gcc python3-dev \
    postgresql-3, postgresql-3-postgis-3, postgresql-server-dev-3, and python3-psycopg3 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry



COPY pyproject.toml poetry.lock /backend/
COPY . ./backend/

RUN poetry install --no-interaction --no-ansi
RUN ./entrypoints/setup-postgis.sh

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "manage.py" , "runserver"]

