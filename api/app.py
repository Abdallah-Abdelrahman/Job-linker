#!/usr/bin/env python3
'''Entry point for flask app'''
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/hello')
def hello():
    '''hello route'''
    return jsonify('Hello World'), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
