from datetime import date, datetime
from typing import Optional

from flask import Blueprint, render_template, request

from app.models import TransactionType
from app.services.analytics import AnalyticsService

bp = Blueprint("reports", __name__)


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


@bp.route("/")
def index():
    date_from = _parse_date(request.args.get("date_from"))
    date_to = _parse_date(request.args.get("date_to"))

    income = AnalyticsService.total_by_type(TransactionType.INCOME, date_from, date_to)
    expense = AnalyticsService.total_by_type(TransactionType.EXPENSE, date_from, date_to)
    profit = income - expense

    income_by_cat = AnalyticsService.by_category(TransactionType.INCOME, date_from, date_to)
    expense_by_cat = AnalyticsService.by_category(TransactionType.EXPENSE, date_from, date_to)
    by_dep = AnalyticsService.by_department(date_from, date_to)

    return render_template(
        "reports/index.html",
        income=income,
        expense=expense,
        profit=profit,
        income_by_cat=income_by_cat,
        expense_by_cat=expense_by_cat,
        by_department=by_dep,
        date_from=date_from,
        date_to=date_to,
    )
