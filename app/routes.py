from flask import render_template, flash, redirect
from app import app 
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
import sqlalchemy as sa
from app import db
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    user={'username':'Rennie'}
    posts=[
        {
            'author':{'username':'John'},
            'body':'Beautiful day in Asheville!'
        },
        {
            'author':{'username':'Susan'},
            'body':'A Face in the Crowd is my favorite movie.'
        }
    ]
    return render_template('index.html', title="Home", user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check.password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title="Sing in", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
