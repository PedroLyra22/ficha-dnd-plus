import os
import re
import uuid

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify, send_from_directory
from app.models import User

bp = Blueprint('main', __name__)

@bp.route('/')
def index():

    return render_template('index.html')

@bp.route('/users')
def index_user():
    users = User.query.all()
    return render_template('user/index.html', users=users)