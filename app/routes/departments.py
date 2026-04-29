from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database import db
from app.models import Department

bp = Blueprint("departments", __name__)


@bp.route("/")
def list_view():
    return render_template("departments/list.html", departments=Department.query.all())


@bp.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"].strip()
        description = request.form.get("description", "").strip()
        if name:
            db.session.add(Department(name=name, description=description))
            db.session.commit()
            flash("Отдел добавлен", "success")
            return redirect(url_for("departments.list_view"))
    return render_template("departments/form.html")


@bp.route("/<int:department_id>/delete", methods=["POST"])
def delete(department_id: int):
    dep = Department.query.get_or_404(department_id)
    db.session.delete(dep)
    db.session.commit()
    return redirect(url_for("departments.list_view"))
