# syntax=docker/dockerfile:1
FROM python:3.8-buster
WORKDIR /flask/frontend
ENV FLASK_APP=frontend
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update
RUN apt-get upgrade
RUN apt-get install inetutils-ping -y
RUN apt-get install traceroute -y
RUN apt-get install iproute2 -y
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
EXPOSE 5000
CMD ["flask", "run","-p","5000"]
