# syntax=docker/dockerfile:1
FROM python:3.8-buster
WORKDIR /flask/backend
ENV FLASK_APP=backend
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install libmariadb-dev -y
RUN apt-get install gnutls-bin -y
RUN apt-get install openssl -y
RUN apt-get install libssl-dev -y
RUN apt-get install build-essential -y
RUN apt-get install python3-dev -y
RUN apt-get install mysql-common -y
RUN apt-get install default-libmysqlclient-dev -y
RUN apt-get install libpq-dev -y
COPY . .
RUN pip install -r requirements.txt
WORKDIR /flask
EXPOSE 5001
CMD ["flask", "run","-p","5001"]
