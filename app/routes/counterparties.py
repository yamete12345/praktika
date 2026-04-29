from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.database import db
from app.models import Counterparty, CounterpartyType

bp = Blueprint("counterparties", __name__)


@bp.route("/")
def list_view():
    return render_template(
        "counterparties/list.html",
        counterparties=Counterparty.query.all(),
    )


@bp.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"].strip()
        type_ = CounterpartyType(request.form["type"])
        if name:
            db.session.add(Counterparty(
                name=name,
                type=type_,
                inn=request.form.get("inn", "").strip(),
                contact=request.form.get("contact", "").strip(),
            ))
            db.session.commit()
            flash("Контрагент добавлен", "success")
            return redirect(url_for("counterparties.list_view"))
    return render_template("counterparties/form.html")


@bp.route("/<int:counterparty_id>/delete", methods=["POST"])
def delete(counterparty_id: int):
    cp = Counterparty.query.get_or_404(counterparty_id)
    db.session.delete(cp)
    db.session.commit()
    return redirect(url_for("counterparties.list_view"))
