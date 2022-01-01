# Building the docker image

docker build -t automommy .

## Run shell

docker run -it automommy bash

from automommy dir

gunicorn --bind :8000 --workers 3 wsgi:application
