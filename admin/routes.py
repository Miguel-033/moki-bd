from flask import Blueprint, render_template, request, redirect, url_for
import json
import os

admin_bp = Blueprint('admin', __name__, template_folder='templates')

DATA_FILE = 'tales.json'

@admin_bp.route('/admin', methods=['GET'])
def admin():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        tales = json.load(f)
    return render_template('admin.html', tales=tales)

@admin_bp.route('/admin/add', methods=['POST'])
def add_tale():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        tales = json.load(f)

    data = request.form
    new_tale = {
        "id": len(tales) + 1,
        "slug": data['slug'],
        "title": data['title'],
        "level": data['level'],
        "genre": data['genre'],
        "text": data['text'],
        "audio_url": data.get('audio_url', '')
    }
    tales.append(new_tale)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tales, f, ensure_ascii=False, indent=2)

    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/delete/<int:id>', methods=['POST'])
def delete_tale(id):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        tales = json.load(f)

    tales = [t for t in tales if t['id'] != id]

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tales, f, ensure_ascii=False, indent=2)

    return redirect(url_for('admin.admin'))
