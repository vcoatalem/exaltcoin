FROM python:3.8

ADD . /app
WORKDIR /app

RUN mkdir -p /exaltcoin_data

RUN pip3 install -r requirements.txt

EXPOSE 8765

CMD ["python3", "server/server.py"]