from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/create-event', methods=['GET', 'POST'])
def create_event():
    # Your function logic here
    return render_template('eventCreation.html')
