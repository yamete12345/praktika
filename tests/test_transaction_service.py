from decimal import Decimal

import pytest

from app.models import Account, Category, TransactionType
from app.services.transaction_service import TransactionService


def test_income_increases_balance(app_ctx):
    account = Account.query.first()
    category = Category.query.filter_by(type=TransactionType.INCOME).first()
    start = Decimal(account.balance)

    TransactionService.create(
        type_=TransactionType.INCOME,
        amount=Decimal("1000.00"),
        category_id=category.id,
        account_id=account.id,
    )

    assert Decimal(account.balance) == start + Decimal("1000.00")


def test_expense_decreases_balance(app_ctx):
    account = Account.query.first()
    category = Category.query.filter_by(type=TransactionType.EXPENSE).first()
    start = Decimal(account.balance)

    TransactionService.create(
        type_=TransactionType.EXPENSE,
        amount=Decimal("500.50"),
        category_id=category.id,
        account_id=account.id,
    )

    assert Decimal(account.balance) == start - Decimal("500.50")


def test_negative_amount_rejected(app_ctx):
    account = Account.query.first()
    category = Category.query.filter_by(type=TransactionType.INCOME).first()

    with pytest.raises(ValueError):
        TransactionService.create(
            type_=TransactionType.INCOME,
            amount=Decimal("-10"),
            category_id=category.id,
            account_id=account.id,
        )


def test_delete_reverts_balance(app_ctx):
    account = Account.query.first()
    category = Category.query.filter_by(type=TransactionType.INCOME).first()
    start = Decimal(account.balance)

    tx = TransactionService.create(
        type_=TransactionType.INCOME,
        amount=Decimal("777"),
        category_id=category.id,
        account_id=account.id,
    )
    TransactionService.delete(tx.id)

    assert Decimal(account.balance) == start
