
from flask import render_template, flash, redirect, request, url_for  # Flask functions for templates, flash messaging, redirects, and URL generation
from app import app, db  # Import the Flask app instance and SQLAlchemy database object
from app.forms import LoginForm  # LoginForm handles user login input and validation
from app.models import User  # User model represents users in the database
from flask_login import current_user, login_user, logout_user, login_required  # Flask-Login utilities for managing authentication
from urllib.parse import urlsplit  # Used to safely parse URLs for security checks
import sqlalchemy as sa  # SQLAlchemy core syntax for building database queries
from app import db
from app.forms import RegistrationForm


# Home page route (default landing page)
@app.route('/')
@app.route('/index')
@login_required  # This decorator ensures the route is only accessible to authenticated users
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Asheville!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'A Face in the Crowd is my favorite movie.'
        }
    ]
    return render_template('index.html', title="Home", user=current_user, posts=posts)

# Login page route (handles GET for form display and POST for login processing)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If already logged in, skip login page
        return redirect(url_for('index'))

    form = LoginForm()  # Create an instance of the login form

    if form.validate_on_submit():  # Only runs if form passes validation
        # Query database for user with matching username
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))

        # If no user found or password check fails, show error and reload page
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')  # Temporary error message
            return redirect(url_for('login'))

        # Log the user in, optionally remembering their session
        login_user(user, remember=form.remember_me.data)

        # Determine where the user should go next after login
        next_page = request.args.get('next')

        # Security check: ensure 'next' is a relative path, not a full URL
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)  # Redirect to the intended page

    # Render the login form page
    return render_template('login.html', title="Sign in", form=form)


# Logout route
@app.route('/logout')
def logout():
    logout_user()  # Clear the session for the logged-in user
    return redirect(url_for('index'))  # Return to home page after logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are registered!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


