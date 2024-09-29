FROM python:3.11-bullseye

RUN adduser \
    --disabled-password \
    --uid 1000 \
    --home /app \
    --gecos '' app \
    && chown -R app /app

# This is what is currently is on rocinante
RUN groupadd -g 139 i2c

RUN usermod -a -G i2c app

RUN apt-get update && \
    apt-get -y upgrade

RUN apt-get -y install --no-install-recommends ddcutil

RUN apt-get clean

USER app

# Install dependencies
RUN pip3 install --user "paho-mqtt"

RUN mkdir -p /app \
    && chown app /app

COPY --chown=app:app . /app

WORKDIR /app

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
CMD ["ddcutil detect"]
#CMD ["python", "-u", "switcher.py"]
