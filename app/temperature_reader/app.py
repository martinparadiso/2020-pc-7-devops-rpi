#!/usr/bin/python3

from flask import Flask
from flask import jsonify
import sensors.temperature

app = Flask(__name__)

@app.route('/')
def sensor():
    ret = {
        "temperature" : sensors.temperature.get_temperature()
    }
    return jsonify(ret)

if __name__ == '__main__':
    app.run()
