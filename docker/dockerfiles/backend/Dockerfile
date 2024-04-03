FROM ubuntu:22.04 as base

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libgdal-dev \
    postgis \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend
RUN mkdir -p /backend

ARG UID=1000
ARG GUID=1000
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off

FROM python:3.10-slim-buster as python-deps

WORKDIR /backend
COPY --from=base /backend /backend

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

FROM python:3.10-slim-bullseye

WORKDIR /backend

COPY --from=python-deps /backend /backend

COPY . ./

RUN pip install --no-cache-dir poetry
RUN rm  -rf .venv && poetry install --no-interaction --no-ansi \
    && poetry run python manage.py collectstatic --noinput

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

