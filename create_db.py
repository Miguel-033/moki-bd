from app import app
from db import db
from models import FairyTale

with app.app_context():
    db.create_all()
    print("База данных и таблица успешно созданы.")
