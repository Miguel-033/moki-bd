from flask import Blueprint, render_template, request, redirect
from models import FairyTale
from db import db

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if request.method == "POST":
        new_tale = FairyTale(
            title=request.form["title"],
            slug=request.form["slug"],
            level=request.form["level"],
            text=request.form["text"],
            audio_url=request.form.get("audio_url", "")
        )
        db.session.add(new_tale)
        db.session.commit()
        return redirect("/admin")

    tales = FairyTale.query.all()
    return render_template("index.html", tales=tales)

@admin_bp.route("/admin/delete/<int:id>", methods=["POST"])
def delete_tale(id):
    tale = FairyTale.query.get(id)
    if tale:
        db.session.delete(tale)
        db.session.commit()
    return redirect("/admin")
