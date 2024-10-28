from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum

# User class
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(100), index=True, unique=True, nullable=False)
    lastname = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan')
    events = db.relationship('Event', backref='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"User(username={self.username})"

# Event class
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(400))
    capacity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(
        Enum('open', 'inactive', 'sold out', 'cancelled', name='event_status'),
        nullable=False,
        default='open'
    )

    # Relationships
    comments = db.relationship('Comment', backref='event', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='event', cascade='all, delete-orphan')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Event(name={self.name}, status={self.status})"

# Comment class
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return f"Comment(text={self.text})"

# Order class
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.now)
    ticket_amount = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    event = db.relationship('Event', back_populates='orders')

    def __init__(self, ticket_amount, event_id, **kwargs):
        super().__init__(**kwargs)
        self.ticket_amount = ticket_amount
        self.event_id = event_id

        # Ensure capacity is sufficient
        event = Event.query.get(event_id)
        if event.capacity < ticket_amount:
            raise ValueError("Not enough tickets available for this event.")
        
        # Update event capacity and calculate total cost
        event.capacity -= ticket_amount
        self.total_cost = self.ticket_amount * event.price

    def __repr__(self):
        return f"Order(id={self.id}, ticket_amount={self.ticket_amount}, total_cost={self.total_cost})"
