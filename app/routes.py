import os
import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, send_from_directory

from app import db
# from app.models import Advertisement, Category

bp = Blueprint('main', __name__)

@bp.route('/')
def index():

    return render_template('index.html')