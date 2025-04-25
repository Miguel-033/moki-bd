from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models import FairyTale, Story
from db import db

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.template_folder = "admin/templates"

db.init_app(app)

@app.route('/')
def home():
    return "Cuentabot API работает!"

# ✅ Временный маршрут инициализации базы
@app.route('/init-db')
def init_db():
    db.create_all()
    return "✅ Таблицы успешно созданы!"

# ========== АДМИНКА ==========

@app.route('/admin', methods=['GET'])
def admin():
    tales = FairyTale.query.all()
    stories = Story.query.all()
    return render_template('admin.html', tales=tales, stories=stories)

@app.route('/admin/add', methods=['POST'])
def admin_add_tale():
    data = request.form
    tale = FairyTale(
        slug=data['slug'],
        title=data['title'],
        level=data['level'],
        genre=data['genre'],
        text=data['text'],
        audio_url=data.get('audio_url', '')
    )
    db.session.add(tale)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/add-story', methods=['POST'])
def admin_add_story():
    data = request.form
    story = Story(
        slug=data['slug'],
        title=data['title'],
        level=data['level'],
        genre=data['genre'],
        text=data['text'],
        audio_url=data.get('audio_url', '')
    )
    db.session.add(story)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
def admin_delete_tale(id):
    tale = FairyTale.query.get(id)
    if tale:
        db.session.delete(tale)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete-story/<int:id>', methods=['POST'])
def admin_delete_story(id):
    story = Story.query.get(id)
    if story:
        db.session.delete(story)
        db.session.commit()
    return redirect(url_for('admin'))

# ========== API ==========

@app.route('/fairy-tales', methods=['GET'])
def get_all_tales():
    tales = FairyTale.query.all()
    return jsonify([{
        'id': t.id,
        'slug': t.slug,
        'title': t.title,
        'level': t.level,
        'genre': t.genre,
        'text': t.text,
        'audio_url': t.audio_url
    } for t in tales])

@app.route('/stories', methods=['GET'])
def get_all_stories():
    stories = Story.query.all()
    return jsonify([{
        'id': s.id,
        'slug': s.slug,
        'title': s.title,
        'level': s.level,
        'genre': s.genre,
        'text': s.text,
        'audio_url': s.audio_url
    } for s in stories])

@app.route('/fairy-tales/<slug>', methods=['GET'])
def get_tale(slug):
    tale = FairyTale.query.filter_by(slug=slug).first()
    if tale:
        return jsonify({
            'id': tale.id,
            'slug': tale.slug,
            'title': tale.title,
            'level': tale.level,
            'genre': tale.genre,
            'text': tale.text,
            'audio_url': tale.audio_url
        })
    return jsonify({'error': 'Сказка не найдена'}), 404

@app.route('/stories/<slug>', methods=['GET'])
def get_story(slug):
    story = Story.query.filter_by(slug=slug).first()
    if story:
        return jsonify({
            'id': story.id,
            'slug': story.slug,
            'title': story.title,
            'level': story.level,
            'genre': story.genre,
            'text': story.text,
            'audio_url': story.audio_url
        })
    return jsonify({'error': 'Рассказ не найден'}), 404

if __name__ == '__main__':
    app.run(debug=True)
