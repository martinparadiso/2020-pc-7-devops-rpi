FROM python:3.8-slim-buster

# Install requirements
RUN apt-get -y update && \
    apt-get -y --no-install-recommends install \
        build-essential && \
    pip3 install --no-cache-dir \
        docker flask gunicorn && \
    apt-get -y remove build-essential && \
    apt-get -y autoremove && \
    apt-get -y clean

# Add the 
COPY ./app/ /app/

EXPOSE 1221
CMD cd app/ && gunicorn -w 1 -b :1221 app:app
