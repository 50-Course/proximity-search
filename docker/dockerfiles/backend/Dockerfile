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

# FROM python:3.10-slim-buster as python-deps (not needed anymore)

WORKDIR /backend
COPY --from=base /backend /backend

# Build final image with GDAL packaged
FROM python:3.10-slim-bullseye

ENV PATH="${PATH}:/usr/local/bin" 

WORKDIR /backend

COPY --from=base /backend /backend
COPY --from=gdal-build . . 

ENV GDAL_LIBRARY_PATH=/usr/local/lib

COPY . .

RUN pip install poetry && \
    poetry config virtualenvs.create true && \
    poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

