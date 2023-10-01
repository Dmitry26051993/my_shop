FROM python:3.10-slim

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
ADD ./requirements.txt .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install sqlite3
RUN mkdir ./src
ADD ./src /src

WORKDIR src
USER user