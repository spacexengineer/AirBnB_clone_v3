#!/usr/bin/python3
from flask import Blueprint, render_template
from api.v1.views.index import *
from api.v1.views import app_views


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")