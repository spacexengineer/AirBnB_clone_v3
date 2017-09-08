#!/usr/bin/python3
"""routes status of app"""
from api.v1.views import app_views
from flask import Flask, render_template, jsonify
import models
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app_views.route('/status')
def status():
    """returns status in json format"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def count_objs():
    """retrieves number of objects by type"""
    json_cls = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']

    # manually find the classes w/ this list, however, method below is better
    # cls = ['Amentity', 'City', 'Place', 'Review', 'State', 'User']

    class_models = sorted(models.CNC)
    class_models.remove('BaseModel')

    cls_count = [storage.count(i) for i in class_models]
    obj_dict = {k: v for k, v in zip(json_cls, cls_count)}
    return jsonify(obj_dict)
