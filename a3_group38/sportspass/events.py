from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, UpdateEventForm, BookTicketForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    form = CommentForm()
    return render_template('events/show.html', event=event, form=form)

# create a new event function
@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            image=db_file_path,
            capacity=form.capacity.data,
            price=form.price.data,
            category=form.category.data,
            status='open',
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.create'))
    return render_template('events/create.html', form=form)

# helper function to check and save uploaded file
def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = '/static/img/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

# comment on an event function
@eventbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, event=event, user=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
    return redirect(url_for('event.show', id=id))

# my events function
@eventbp.route('/my-events')
@login_required
def my_events():
    events = db.session.scalars(db.select(Event).where(Event.user_id == current_user.id)).all()
    return render_template('events/user-events.html', events=events)

# update event function
@eventbp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event.user_id != current_user.id:
        flash("You are not authorized to update this event.", "danger")
        return redirect(url_for('event.show', id=id))

    form = UpdateEventForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.date = form.date.data
        event.location = form.location.data
        event.price = form.price.data
        event.capacity = form.capacity.data
        event.category = form.category.data
        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect(url_for('event.show', id=id))
    
    return render_template('events/update.html', form=form, event=event)

# cancel event function
@eventbp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_event(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if event.user_id != current_user.id:
        flash("You are not authorized to cancel this event.", "danger")
        return redirect(url_for('event.show', id=id))
    
    # Check if the event is already inactive
    if event.status == 'inactive':
        flash('This event is inactive and cannot be canceled.', 'danger')
        return redirect(url_for('event.show', id=event.id))

    event.status = 'cancelled'
    db.session.commit()
    flash("Event has been cancelled.", "success")
    return redirect(url_for('event.show', id=id))

# book tickets
@eventbp.route('/<int:event_id>/book', methods=['GET', 'POST'])
@login_required
def book_tickets(event_id):
    form = BookTicketForm()
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))

    if event.status in ['cancelled', 'inactive', 'sold out']:
        flash('This event is not available for booking.', 'danger')
        return redirect(url_for('event.show', id=event.id))

    if form.validate_on_submit():
        ticket_amount = form.ticket_amount.data
        total_cost = event.price * ticket_amount

        # Check if enough tickets are available
        if ticket_amount > event.capacity:
            flash('Not enough tickets available for this event.', 'warning')
            return render_template('events/book-tickets.html', form=form, event=event)

        order_date = datetime.now()

        # Create a new order
        new_order = Order(
            ticket_amount=ticket_amount,
            total_cost=total_cost,
            order_date=order_date,
            user_id=current_user.id,
            event_id=event.id
        )

        # Update event capacity and status
        event.capacity -= ticket_amount
        if event.capacity <= 0:
            event.capacity = 0
            event.status = 'sold out'

        # Save the order and commit all changes
        db.session.add(new_order)
        db.session.commit()

        flash(f'Order placed successfully! Your order ID is {new_order.id}.', 'success')
        return redirect(url_for('event.show', id=event.id))

    return render_template('events/book-tickets.html', form=form, event=event)


# booking history function
@eventbp.route('/booking-history')
@login_required
def booking_history():
    bookings = db.session.scalars(db.select(Order).where(Order.user_id == current_user.id)).all()
    
    # Add a custom order ID to each booking dynamically
    for booking in bookings:
        # Get the first letter of the user's username
        first_letter = current_user.username[0].upper()

        # Format the order date as YYYYMMDD
        date_str = booking.order_date.strftime('%Y%m%d')

        # Use the database `id` to ensure uniqueness
        booking.custom_order_id = f"{first_letter}{date_str}-{booking.id}"

    return render_template('events/booking-history.html', bookings=bookings)

