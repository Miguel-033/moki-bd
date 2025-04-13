from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models import FairyTale
from db import db

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
CORS(app)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.template_folder = "admin/templates"  # Путь к HTML-шаблонам

db.init_app(app)

@app.route('/')
def home():
    return "Cuentabot API работает!"

# ========== АДМИН ПАНЕЛЬ ==========

@app.route('/admin', methods=['GET'])
def admin():
    tales = FairyTale.query.all()
    return render_template('admin.html', tales=tales)

@app.route('/admin/add', methods=['POST'])
def admin_add():
    data = request.form
    tale = FairyTale(
        slug=data['slug'],
        title=data['title'],
        level=data['level'],
        text=data['text'],
        audio_url=data.get('audio_url', '')
    )
    db.session.add(tale)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
def admin_delete(id):
    tale = FairyTale.query.get(id)
    if tale:
        db.session.delete(tale)
        db.session.commit()
    return redirect(url_for('admin'))

# ========== API ==========

@app.route('/fairy-tales', methods=['GET'])
def get_all_stories():
    tales = FairyTale.query.all()
    return jsonify([{
        'id': t.id,
        'slug': t.slug,
        'title': t.title,
        'level': t.level,
        'text': t.text,
        'audio_url': t.audio_url
    } for t in tales])

@app.route('/fairy-tales/<slug>', methods=['GET'])
def get_story(slug):
    tale = FairyTale.query.filter_by(slug=slug).first()
    if tale:
        return jsonify({
            'id': tale.id,
            'slug': tale.slug,
            'title': tale.title,
            'level': tale.level,
            'text': tale.text,
            'audio_url': tale.audio_url
        })
    return jsonify({'error': 'Сказка не найдена'}), 404

@app.route('/fairy-tales', methods=['POST'])
def add_story():
    data = request.get_json()
    tale = FairyTale(
        slug=data['slug'],
        title=data['title'],
        level=data['level'],
        text=data['text'],
        audio_url=data.get('audio_url', '')
    )
    db.session.add(tale)
    db.session.commit()
    return jsonify({'message': 'Сказка добавлена успешно'}), 201

@app.route('/fairy-tales/<int:id>', methods=['DELETE'])
def delete_story(id):
    tale = FairyTale.query.get(id)
    if tale:
        db.session.delete(tale)
        db.session.commit()
        return jsonify({'message': 'Сказка удалена'}), 200
    return jsonify({'error': 'Сказка не найдена'}), 404

if __name__ == '__main__':
    app.run(debug=True)
