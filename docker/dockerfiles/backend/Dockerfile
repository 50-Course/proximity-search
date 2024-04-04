FROM ubuntu:22.04 as base

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    postgis \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend
RUN mkdir -p /backend

ARG UID=1000
ARG GUID=1000
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off


# Build GDAL Alpine-based image
FROM ghcr.io/osgeo/gdal:alpine-normal-latest as gdal-build

# ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so \
#     GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so \
#     PROJ_LIBRARY_PATH=/usr/lib/libproj.so

FROM python:3.10-slim-buster as python-deps

WORKDIR /backend
COPY --from=base /backend /backend
COPY --from=gdal-build ./ ./

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

# Build final image with GDAL packaged
# NOTE: we have to install GDAL from source to avoid issues with the pre-built wheels
FROM python:3.10-slim-bullseye

ENV PATH="${PATH}:/usr/local/bin:/usr/.poetry/bin"

WORKDIR /backend

COPY --from=python-deps /backend /backend

COPY . ./

# RUN poetry run python manage.py collectstatic --noinput

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

