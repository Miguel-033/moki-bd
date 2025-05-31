from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import os

app = Flask(__name__)
app.template_folder = "admin/templates"

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"tales": [], "stories": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    return "✅ Cuentabot API работает без базы данных!"

@app.route('/fairy-tales')
def get_fairy_tales():
    data = load_data()
    return jsonify(data.get("tales", []))

@app.route('/stories')
def get_stories():
    data = load_data()
    return jsonify(data.get("stories", []))

@app.route('/fairy-tales/<slug>')
def get_fairy_tale(slug):
    data = load_data()
    tale = next((t for t in data.get("tales", []) if t['slug'] == slug), None)
    if tale:
        return jsonify(tale)
    return jsonify({"error": "Сказка не найдена"}), 404

@app.route('/stories/<slug>')
def get_story(slug):
    data = load_data()
    story = next((s for s in data.get("stories", []) if s['slug'] == slug), None)
    if story:
        return jsonify(story)
    return jsonify({"error": "Рассказ не найден"}), 404

# ========== АДМИНКА ==========

@app.route('/admin', methods=['GET'])
def admin_panel():
    data = load_data()
    return render_template("admin.html", tales=data.get("tales", []), stories=data.get("stories", []))

@app.route('/admin/add', methods=['POST'])
def add_fairy_tale():
    data = load_data()
    form = request.form
    new_tale = {
        "title": form["title"],
        "slug": form["slug"],
        "level": form["level"],
        "genre": form["genre"],
        "text": form["text"],
        "audio_url": form.get("audio_url", "")
    }
    data["tales"].append(new_tale)
    save_data(data)
    return redirect(url_for("admin_panel"))

@app.route('/admin/add-story', methods=['POST'])
def add_story():
    data = load_data()
    form = request.form
    new_story = {
        "title": form["title"],
        "slug": form["slug"],
        "level": form["level"],
        "genre": form["genre"],
        "text": form["text"],
        "audio_url": form.get("audio_url", "")
    }
    data["stories"].append(new_story)
    save_data(data)
    return redirect(url_for("admin_panel"))

@app.route('/admin/delete/<slug>', methods=['POST'])
def delete_fairy_tale(slug):
    data = load_data()
    data["tales"] = [t for t in data["tales"] if t["slug"] != slug]
    save_data(data)
    return redirect(url_for("admin_panel"))

@app.route('/admin/delete-story/<slug>', methods=['POST'])
def delete_story(slug):
    data = load_data()
    data["stories"] = [s for s in data["stories"] if s["slug"] != slug]
    save_data(data)
    return redirect(url_for("admin_panel"))

if __name__ == "__main__":
    app.run(debug=True)
