#!/usr/bin/python3
"""Starts API"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """close app"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """returns custom error in json format"""
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    """Where the Flask runs"""
    app.run(host='0.0.0.0', port=5000)
