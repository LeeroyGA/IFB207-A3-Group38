from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event

#from .models import Destination
from .models import User
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # events = db.session.scalars(db.select(Event)).all() 

    featured_events = Event.query.order_by(Event.date).limit(3).all()   
    
    # Get the search query from the request
    search_query = request.args.get('search', '')  # Default is an empty string if no query
    selected_category = request.args.get('category', 'all')

    # Query distinct categories from the 'events' table
    categories = db.session.scalars(db.select(Event.category).distinct()).all()

    # Filter events based on search term and category
    query = db.select(Event)

    if search_query:
        query = query.where(Event.name.ilike(f'%{search_query}%') | Event.description.ilike(f'%{search_query}%'))
    
    if selected_category != 'all':
        query = query.where(Event.category == selected_category)

    events = db.session.scalars(query).all()


    return render_template('index.html', events=events, featured_events=featured_events, categories=categories)


