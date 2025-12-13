from main import app
from utils.database import db

with app.app_context():
    db.create_all()