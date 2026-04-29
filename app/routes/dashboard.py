from datetime import date

from flask import Blueprint, render_template

from app.models import Account, Transaction, TransactionType
from app.services.analytics import AnalyticsService

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def index():
    today = date.today()
    year_start = date(today.year, 1, 1)

    income = AnalyticsService.total_by_type(TransactionType.INCOME, year_start, today)
    expense = AnalyticsService.total_by_type(TransactionType.EXPENSE, year_start, today)
    profit = income - expense

    accounts = Account.query.all()
    recent = Transaction.query.order_by(Transaction.date.desc()).limit(10).all()
    monthly = AnalyticsService.monthly_trend(today.year)

    return render_template(
        "dashboard.html",
        income=income,
        expense=expense,
        profit=profit,
        accounts=accounts,
        recent=recent,
        monthly=monthly,
        year=today.year,
    )
