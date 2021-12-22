FROM debian:latest
USER root

WORKDIR /app
COPY . /app

RUN apt update && apt install libglib2.0-dev bluez python3-pip -y

RUN pip3 install -r requirements.txt

CMD ["python3", "/app/main.py"]