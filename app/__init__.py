from flask import Flask
from flask_login import LoginManager

from .config import Configuration
from .models import db, Employee
from .routes import orders, session

app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)
db.init_app(app)

# Configure LoginManager
login = LoginManager(app)
# Automatically redirects protected pages to the login page
login.login_view = "session.login"


# Get Employee objects from the database
@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))