# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /microservices/feed_service
ENV FLASK_APP=feed_service
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache g++ gcc musl-dev linux-headers
COPY . .
RUN pip install -r requirements.txt
WORKDIR /microservices
RUN python3 -m feed_service.script
EXPOSE 5002
CMD ["flask", "run","-p","5002"]
