FROM python:3.10.11-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/MaksiX/Social_Network_MaksiX

COPY requirements-docker.txt /usr/src/MaksiX/requirements.txt
RUN pip install -r ../requirements.txt

COPY . /usr/src/MaksiX
COPY /Social_Network_MaksiX/.env.docker /usr/src/MaksiX/Social_Network_MaksiX/.env
