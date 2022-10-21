FROM python:3.10-slim-bullseye

WORKDIR /app

COPY src/ ./

RUN apt update
RUN apt install default-libmysqlclient-dev -y

RUN pip3 install -r requirements.txt

RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o wait-for-it.sh
RUN chmod +x wait-for-it.sh

EXPOSE 8080
