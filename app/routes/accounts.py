from decimal import Decimal

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database import db
from app.models import Account

bp = Blueprint("accounts", __name__)


@bp.route("/")
def list_view():
    return render_template("accounts/list.html", accounts=Account.query.all())


@bp.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"].strip()
        balance = Decimal(request.form.get("balance", "0").replace(",", ".") or "0")
        if name:
            db.session.add(Account(name=name, balance=balance))
            db.session.commit()
            flash("Счёт добавлен", "success")
            return redirect(url_for("accounts.list_view"))
    return render_template("accounts/form.html")


@bp.route("/<int:account_id>/delete", methods=["POST"])
def delete(account_id: int):
    acc = Account.query.get_or_404(account_id)
    db.session.delete(acc)
    db.session.commit()
    return redirect(url_for("accounts.list_view"))
