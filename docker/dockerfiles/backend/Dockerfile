FROM python:3.12.0-slim-buster as base

ARG UID=1000
ARG GUID=1000

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR off

FROM base as builder
RUN apt-get update && apt-get install -y \
    --no-install-recommends build-essential gcc python3-dev \
    postgresql-3, postgresql-3-postgis-3, postgresql-server-dev-3, and python3-psycopg3 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN  pip install poetry


WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev
RUN ./entrypoints/setup-postgis.sh

ENTRYPOINT ["poetry", "run", "python", "manage.py" , "runserver"]
