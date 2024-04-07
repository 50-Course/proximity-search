#!/usr/bin/env sh
# This script creates PostGIS extension in a PostgreSQL database.

set -e

# Set terminal colors
COLOR_ERR='\033[0;31m'
COLOR_OKAY='\033[0;32m'
COLOR_NC='\033[0m'

create_postgis_extension() {
    psql -h localhost -U postgres -p 5432 -d spatial_db_postgis -c "CREATE EXTENSION postgis;"
    psql -h localhost -U postgres -p 5432 -d spatial_db_postgis -c "CREATE EXTENSION postgis_topology;"
}

#  Use colors to indicate the status of the script
echo ${COLOR_OKAY}"Creating PostGIS extension in PostgreSQL database..."}${COLOR_NC}

if [ -z "$PGPASSWORD" ]; then
  echo ${COLOR_ERR}"Please set the PGPASSWORD environment variable."}${COLOR_NC}
  exit 1
fi

create_postgis_extension

echo %{COLOR_OKAY}"PostGIS extension created in PostgreSQL database."}${COLOR_NC}
