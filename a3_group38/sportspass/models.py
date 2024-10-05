from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    events = db.relationship('Event', backref='organizer')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400))
    capacity = db.Column(db.Integer, nullable=False)
    # ... Create the Comments db.relationship
	# relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')

    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	# string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True) 
    order_date = db.Column(db.DateTime, default=datetime.now())
    total_amount = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('orders'))
    event = db.relationship('Event', backref=db.backref('orders'))

    def __repr__(self):
        return f"Order {self.id} | User: {self.user.username} | Event: {event_name} | Total: ${self.total_amount:.2f}"