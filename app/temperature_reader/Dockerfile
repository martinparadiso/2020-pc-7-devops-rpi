FROM python:3.8-slim-buster

RUN apt-get -y update && \
    apt-get -y --no-install-recommends install \
        build-essential python3-dev python3-smbus && \
    pip3 install --no-cache-dir adafruit-circuitpython-ads1x15 RPi.GPIO flask gunicorn && \
    apt-get -y remove build-essential python3-dev && \
    apt-get -y autoremove && \
    apt-get -y clean

COPY . app/
WORKDIR /app/
CMD exec gunicorn -w 1 -b :1221 app:app
