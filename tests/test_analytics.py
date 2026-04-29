from decimal import Decimal

from app.models import Account, Category, TransactionType
from app.services.analytics import AnalyticsService
from app.services.transaction_service import TransactionService


def _seed(app_ctx):
    account = Account.query.first()
    income_cat = Category.query.filter_by(type=TransactionType.INCOME).first()
    expense_cat = Category.query.filter_by(type=TransactionType.EXPENSE).first()
    TransactionService.create(TransactionType.INCOME, Decimal("1000"), income_cat.id, account.id)
    TransactionService.create(TransactionType.EXPENSE, Decimal("300"), expense_cat.id, account.id)


def test_profit(app_ctx):
    _seed(app_ctx)
    assert AnalyticsService.profit() == Decimal("700")


def test_total_income(app_ctx):
    _seed(app_ctx)
    assert AnalyticsService.total_by_type(TransactionType.INCOME) == Decimal("1000")


def test_by_category(app_ctx):
    _seed(app_ctx)
    rows = AnalyticsService.by_category(TransactionType.EXPENSE)
    assert any(r["total"] == 300.0 for r in rows)
