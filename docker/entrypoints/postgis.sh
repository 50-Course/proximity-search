#!/usr/bin/env sh
# This script creates PostGIS extension in a PostgreSQL database.

set -e

update_dependencies() {
  apt-get update -y && apt-get install -y postgresql-13-postgis-3
}

create_postgis_extension() {
  createdb -U spatialdb 
  psql -U spatialdb -c "CREATE EXTENSION postgis;"
  psql -U spatialdb -c "CREATE EXTENSION postgis_topology;"
}

echo "Updating dependencies..."

update_dependencies

echo "Creating PostGIS extension in PostgreSQL database..."

create_postgis_extension

echo "PostGIS extension created in PostgreSQL database."
