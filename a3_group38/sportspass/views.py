from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event

#from .models import Destination
from .models import User
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()    
    return render_template('index.html', events=events)
