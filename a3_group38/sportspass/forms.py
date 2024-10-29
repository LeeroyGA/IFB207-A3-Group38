from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, IntegerField, SubmitField, StringField, PasswordField, DateTimeField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# new event form
class EventForm(FlaskForm):
    name = StringField('Event Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    date = DateTimeField('Event Date (DD/MM/YYYY hh:mm AM/PM)', validators=[InputRequired()], format='%d/%m/%Y %I:%M %p')
    location = StringField('Location', validators=[InputRequired()])
    price = IntegerField('Price ($)', validators=[InputRequired()])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    capacity = IntegerField('Capacity', validators=[
        InputRequired(),
        NumberRange(min=1, message='Capacity must be a positive integer')
    ])
    category = StringField('Category', validators=[InputRequired()])
    submit = SubmitField("Create")

# update event form (for updating event details by the owner, excluding status)
class UpdateEventForm(FlaskForm):
    name = StringField('Event Title', validators=[InputRequired()])
    description = TextAreaField('Description')
    date = DateTimeField('Event Date (DD/MM/YYYY hh:mm AM/PM)', validators=[InputRequired()], format='%d/%m/%Y %I:%M %p')
    location = StringField('Location', validators=[InputRequired()])
    price = IntegerField('Price ($)', validators=[InputRequired()])
    capacity = IntegerField('Capacity', validators=[
        InputRequired(),
        NumberRange(min=1, message='Capacity must be a positive integer')
    ])
    category = StringField('Category', validators=[InputRequired()])
    submit = SubmitField("Update Event")

# cancel event form (for canceling the event)
class CancelEventForm(FlaskForm):
    submit = SubmitField("Cancel Event")

# creates the login information
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired(),
                      EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# user comment
class CommentForm(FlaskForm):
    text = TextAreaField('Add Comment', [InputRequired()])
    submit = SubmitField('Post')

# book ticket
class BookTicketForm(FlaskForm):
    ticket_amount = IntegerField('Number of Tickets', validators=[
        InputRequired(), NumberRange(min=1, message="Please book at least one ticket.")
    ])
    submit = SubmitField('Book Tickets')
