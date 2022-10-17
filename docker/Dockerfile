FROM --platform=linux/amd64 python:3.10.5

LABEL \
  maintainer="Adil Rashitov <adil@wastelabs.co>" \
  org.opencontainers.image.title="dev_veolia_uk_backend" \
  org.opencontainers.image.description="Dockerfile of veolia backend" \
  org.opencontainers.image.authors="Adil Rashitov <adil@wastelabs.co>" \
  org.opencontainers.image.url="https://github.com/AtmosOne/dev_veolia_uk_backend"

WORKDIR /dev_veolia_uk_backend

ENV PYTHONPATH "${PYTHONPATH}:/home/newuser/.local/bin"
ENV PYTHONPATH "${PYTHONPATH}:${PWD}/"
ENV PATH "${PATH}:${PWD}/"
ENV POETRY_VIRTUALENVS_CREATE=false


COPY ./ ./

RUN pip3 install --upgrade pip && pip3 install wheel poetry && poetry install


HEALTHCHECK --interval=1m --timeout=5s \
  CMD curl -f http://localhost:8000/healthcheck || exit 1

EXPOSE 8000
