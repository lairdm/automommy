# syntax=docker/dockerfile:1
FROM python:3.8-slim-bullseye

RUN adduser \
    --disabled-password \
    --uid 1000 \
    --home /code \
    --gecos '' client \
    && chown -R client /code

WORKDIR /code

RUN mkdir -p /torrents \
    && chown client /torrents

RUN mkdir -p /code/.ssh \
    && chown client /code/.ssh

COPY bin/install-packages.sh /code/
RUN ./install-packages.sh

USER client

ENV PYTHONDONTWRITEBYTECODE=1 \
    PATH="/code/.local/bin:${PATH}" \
    PYTHONPATH="/code"
ENV PYTHONUNBUFFERED=1

COPY --chown=client:client requirements.txt /code/

RUN pip install --user -r requirements.txt

COPY --chown=client:client transmission/config /code/.ssh/

COPY --chown=client:client . /code/

EXPOSE 8000

WORKDIR /code/automommy

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "wsgi:application"]