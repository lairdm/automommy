#!/usr/bin/env bash

echo "SELECT 'CREATE DATABASE ${PGDATABASE:-automommy}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${PGDATABASE:-automommy}')\gexec" | psql postgres

cat /code/schema/schema.sql | psql

cd /code

python manage.py migrate
