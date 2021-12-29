FROM debian:latest
USER root

WORKDIR /app
COPY ./server /app

RUN apt-get update && apt-get install python3 libglib2.0-dev bluez python3-pip -y

COPY ./client/dist /app/static

RUN pip3 install -r requirements.txt

CMD ["python3", "./app.py"]
