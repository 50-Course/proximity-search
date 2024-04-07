FROM ubuntu:22.04 as base

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    binutils \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    gdal-bin \
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
COPY --from=gdal-build /usr/local /usr/local

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

# Build final image with GDAL packaged
# NOTE: we have to install GDAL from source to avoid issues with the pre-built wheels
FROM python:3.10-slim-bullseye

ENV PATH="${PATH}:/usr/local/bin"

RUN apt-get update && apt-get install -y --no-install-recommends libgdal-dev

WORKDIR /backend

COPY --from=python-deps /backend /backend

COPY . ./

RUN pip install poetry && \
    poetry config virtualenvs.create true && \
    poetry install --no-interaction --no-ansi

RUN pip wheel --no-cache-dir --use-pep517 "gdal (==3.4.1)"
RUN poetry run python manage.py collectstatic --noinput

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

