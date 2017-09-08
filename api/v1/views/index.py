#!/usr/bin/python3
"""routes status of app"""
from api.v1.views import app_views
from flask import Flask, render_template, jsonify
app = Flask(__name__)


@app_views.route('/status')
def status():
    """returns status in json format"""
    return jsonify(status="OK")
