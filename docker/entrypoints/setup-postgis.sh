#!/usr/bin/env sh

set -e

echo "Creating PostGIS extension in PostgreSQL database..."
# This script creates PostGIS extension in a PostgreSQL database.
# It is intended to be used in a Docker container.
createdb -U spatialdb -E UTF8 
psql -U spatialdb -c "CREATE EXTENSION postgis;"
psql -U spatialdb -c "CREATE EXTENSION postgis_topology;"

echo "PostGIS extension created in PostgreSQL database."
exit 0
