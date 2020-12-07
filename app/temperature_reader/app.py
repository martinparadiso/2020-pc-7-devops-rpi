#!/usr/bin/python3

from flask import Flask, jsonify, render_template
import sensors.temperature

app = Flask(__name__)

@app.route('/')
def sensor():
    ret = {
        "temperature" : sensors.temperature.get_temperature()
    }
    return jsonify(ret)

@app.route('/ui')
def ui():
    
    return render_template('ui.html', temperature=sensors.temperature.get_temperature())

if __name__ == '__main__':
    app.run()
