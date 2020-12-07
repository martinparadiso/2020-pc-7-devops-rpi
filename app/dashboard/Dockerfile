FROM python:3.8-slim-buster

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./project /app
WORKDIR /app
CMD ["sh", "-c", "python3 setup.py ; exec gunicorn project.wsgi -b :80"]
