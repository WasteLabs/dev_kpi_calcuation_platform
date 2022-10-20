FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9

LABEL \
  maintainer="Adil Rashitov <adil@wastelabs.co>" \
  title="dev_kpi_calculation_platform" \
  description="Dockerfile of KPI calculation platform" \
  authors="Adil Rashitov <adil@wastelabs.co>" \
  url="https://github.com/WasteLabs/dev_kpi_calculation_platform"

WORKDIR /app
# ARG LAMBDA_TASK_ROOT="/research_aws_lambda/src"

ENV PYTHONPATH "${PYTHONPATH}:/home/newuser/.local/bin"
ENV PYTHONPATH "${PYTHONPATH}:${PWD}/"
ENV PATH "${PATH}:${PWD}/"
ENV POETRY_VIRTUALENVS_CREATE=false

COPY ./ ./

RUN pip3 install --upgrade pip && pip3 install wheel poetry && poetry install --only main


CMD [ "src/aws_lambda/kpi/main.handler" ]
EXPOSE 8080
