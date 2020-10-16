FROM locustio/locust

ARG CODE_DIR=./code
ARG DOCKER_DIR=./app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY $CODE_DIR /mnt/locust/