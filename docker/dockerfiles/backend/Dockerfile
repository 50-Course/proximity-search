FROM python:3.10-slim-bullseye as build-stage

ARG UID=1000
ARG GUID=1000

WORKDIR /backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off  \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y \
    --no-install-recommends build-essential gcc python3-dev \
    postgresql-3, postgresql-3-postgis-3, postgresql-server-dev-3, and python3-psycopg3 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock /backend/
COPY backend/ .

RUN poetry install --no-interaction --no-ansi
RUN ./entrypoints/setup-postgis.sh

RUN poetry run python manage.py collectstatic --noinput


# Run application as lightweight as possible
FROM python:3.10-slim-bullseye

WORKDIR /backend
COPY --from=build-stage /backend /backend

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "python", "manage.py" , "runserver", "0.0.0.0:8000"]

