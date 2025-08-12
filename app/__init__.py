from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
# Added this chunk from AI to make running flask shell easier

@app.shell_context_processor
def make_shell_context():
    # Import inside the function to avoid circular imports during app initialization
    from app.models import User
    return {'db': db, 'User': User}
