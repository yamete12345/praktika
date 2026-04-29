from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database import db
from app.models import Category, TransactionType

bp = Blueprint("categories", __name__)


@bp.route("/")
def list_view():
    return render_template("categories/list.html", categories=Category.query.all())


@bp.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"].strip()
        type_ = TransactionType(request.form["type"])
        if name:
            db.session.add(Category(name=name, type=type_))
            db.session.commit()
            flash("Категория добавлена", "success")
            return redirect(url_for("categories.list_view"))
    return render_template("categories/form.html")


@bp.route("/<int:category_id>/delete", methods=["POST"])
def delete(category_id: int):
    cat = Category.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for("categories.list_view"))
