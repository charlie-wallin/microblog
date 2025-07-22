import os

# Define the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key for securing forms (CSRF protection, etc.)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database URI: use DATABASE_URL if set, else default to SQLite in the base directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

