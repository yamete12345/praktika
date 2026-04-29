from decimal import Decimal, InvalidOperation
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.models import (
    Transaction, Category, Account, Department, Counterparty, TransactionType,
)
from app.services.transaction_service import TransactionService

bp = Blueprint("transactions", __name__)


@bp.route("/")
def list_view():
    txs = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template("transactions/list.html", transactions=txs)


@bp.route("/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            amount = Decimal(request.form["amount"].replace(",", "."))
            type_ = TransactionType(request.form["type"])
            tx_date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
            TransactionService.create(
                type_=type_,
                amount=amount,
                category_id=int(request.form["category_id"]),
                account_id=int(request.form["account_id"]),
                department_id=int(request.form["department_id"]) or None
                    if request.form.get("department_id") else None,
                counterparty_id=int(request.form["counterparty_id"]) or None
                    if request.form.get("counterparty_id") else None,
                description=request.form.get("description"),
                tx_date=tx_date,
            )
            flash("Транзакция добавлена", "success")
            return redirect(url_for("transactions.list_view"))
        except (ValueError, InvalidOperation) as e:
            flash(f"Ошибка: {e}", "error")

    return render_template(
        "transactions/form.html",
        categories=Category.query.all(),
        accounts=Account.query.all(),
        departments=Department.query.all(),
        counterparties=Counterparty.query.all(),
    )


@bp.route("/<int:transaction_id>/delete", methods=["POST"])
def delete(transaction_id: int):
    TransactionService.delete(transaction_id)
    flash("Транзакция удалена", "success")
    return redirect(url_for("transactions.list_view"))
