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
    comments = db.relationship('Comment', backref='user')
    events = db.relationship('Event', backref='user')
    orders = db.relationship('Order', backref='user')

    def __repr__(self):
        return f"Name: {self.username}"

# Event class
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(400))
    capacity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Add 'category' field
    status = db.Column(
        Enum('open', 'inactive', 'sold out', 'cancelled', name='event_status'),
        nullable=False,
        default='open'
    )
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    orders = db.relationship('Order', back_populates='event')

    def __repr__(self):
        return f"Name: {self.name}"
    
# Comment class
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"

# Order class
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True) 
    order_date = db.Column(db.DateTime, default=datetime.now)
    ticket_amount = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    event = db.relationship('Event', back_populates='orders')

    # Constructor
    def __init__(self, ticket_amount, event_id, **kwargs):
        super().__init__(**kwargs)
        self.ticket_amount = ticket_amount
        self.event_id = event_id

        if self.event.capacity < ticket_amount:
            raise ValueError("Not enough tickets available for this event.")
        
        self.event.capacity -= ticket_amount
        self.total_cost = self.ticket_amount * self.event.price
    
    def __repr__(self):
        return f"Order {self.id} | User: {self.user.name} | Event: {self.event.name} | Total: ${self.total_amount:.2f}"