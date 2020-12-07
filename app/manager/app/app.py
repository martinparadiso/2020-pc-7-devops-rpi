#!/usr/bin/python3.8

from flask import Flask, request, jsonify   # flask for the server
from multiprocessing import Lock            # Lock for concurrent requests
from flask_httpauth import HTTPTokenAuth    # For token auth
import container
import os

# Locks
test_lock = Lock()
app = Flask(__name__)

container = container.Container()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    f"{os.environ['ACCESS_TOKEN']}" : "user"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

# Routes =======================================================================

@app.route('/tag', methods=['POST'])
@auth.login_required
def use():
    """
    Change the tag of the image used by this device
    """
    content = request.json
    new_tag = content['tag']
    container.switch_version(new_tag)
    return jsonify({"success" : True})

@app.route('/tag', methods=['GET'])
@auth.login_required
def version():
    """
    Get the version (tag) used by this device
    """
    t = container.tag
    return jsonify({ "tag" : t })

@app.route('/status')
@auth.login_required
def status():
    stat = container.status()
    return jsonify({
        'status' : str(stat)
    })

@app.route('/image')
@auth.login_required
def image():
    img = container.image
    return jsonify({
        'image' : str(img)
    })

@app.route('/force_update', methods=['POST'])
@auth.login_required
def force_update():
    container.force_update()
    return jsonify({"success" : True})

if __name__ == '__main__':
    app.run()
