# Building the docker image

docker build -t automommy .

## Run shell

docker run -it automommy bash

from automommy dir

gunicorn --bind :8000 --workers 3 wsgi:application

## Initial deployment

To create the database and apply the migrations, this can be run with the stack down.

docker-compose -f docker-migrate.yaml up --abort-on-container-exit --exit-code-from migration
