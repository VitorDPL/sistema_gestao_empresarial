from projeto import app, db
from flask import request, jsonify, render_template, redirect, url_for
from projeto.models import *

@app.route('/')
def index():
    return render_template('index.html')