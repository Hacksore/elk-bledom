FROM node:latest as builder

WORKDIR /app
COPY ./client .

RUN npm ci && npm run build

FROM debian:latest
USER root

WORKDIR /app
COPY ./server /app

COPY --from=builder /app/dist /app/static

RUN apt update && apt install libglib2.0-dev bluez python3-pip -y

RUN pip3 install -r requirements.txt

ENV FLASK_APP=app

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app"]
