FROM python:3.9-slim-bullseye

WORKDIR /app

COPY src/ ./

RUN apt update
RUN apt install default-libmysqlclient-dev -y

RUN pip3 install -r requirements.txt

ADD wait-for-it.sh ./
RUN chmod +x wait-for-it.sh

EXPOSE 8080
