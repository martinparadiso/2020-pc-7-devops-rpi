FROM debian:10

RUN apt update -y && apt upgrade -y && apt install -y build-essential python3-dev python3-smbus python3-pip wget
RUN pip3 install adafruit-circuitpython-ads1x15 RPi.GPIO flask

COPY . app/

WORKDIR app/

CMD FLASK_APP=app python3 -m flask run --host 0.0.0.0 
