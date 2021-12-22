FROM ubuntu:18.04
USER root

WORKDIR /app
COPY . /app

RUN apt update && apt install bluez python3-pip -y

RUN pip3 install -r requirements.txt

CMD ["python3", "/app/main.py"]