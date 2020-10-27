FROM locustio/locust

ARG CODE_DIR=./code
ARG DOCKER_DIR=./app

USER root
RUN apt-get update && \
    apt-get install -y chromium-driver chromium

USER locust
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY $CODE_DIR /mnt/locust/