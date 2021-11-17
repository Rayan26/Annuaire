# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /microservices/front_service
ENV FLASK_APP=front_service
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache g++ gcc musl-dev linux-headers
COPY . .
RUN pip install -r requirements.txt
WORKDIR /microservices
EXPOSE 5000
CMD ["flask", "run","-p","5000"]
