from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FairyTale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(10), nullable=False)
    genre = db.Column(db.String(50), nullable=False)  # 🔥 добавили genre
    text = db.Column(db.Text, nullable=False)
    audio_url = db.Column(db.String(500), nullable=True)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    level = db.Column(db.String(10), nullable=False)
    genre = db.Column(db.String(50), nullable=False)  # 🔥 добавили genre
    text = db.Column(db.Text, nullable=False)
    audio_url = db.Column(db.String(500), nullable=True)
