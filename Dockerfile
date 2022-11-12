FROM python:3.10-slim-bullseye

WORKDIR /app

COPY src/ ./src
COPY .env ./
COPY poetry.lock ./
COPY pyproject.toml ./
COPY cert.pem ./

RUN apt update
RUN apt install default-libmysqlclient-dev curl -y
RUN touch README.md

RUN pip3 install poetry
RUN poetry install --no-dev

RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o wait-for-it.sh
RUN chmod +x wait-for-it.sh

EXPOSE 8000
