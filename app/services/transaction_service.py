from datetime import date
from decimal import Decimal
from typing import Optional

from app.database import db
from app.models import Transaction, Account, TransactionType


class TransactionService:
    """Бизнес-логика работы с транзакциями и обновления балансов счетов."""

    @staticmethod
    def create(
        type_: TransactionType,
        amount: Decimal,
        category_id: int,
        account_id: int,
        tx_date: Optional[date] = None,
        department_id: Optional[int] = None,
        counterparty_id: Optional[int] = None,
        description: Optional[str] = None,
    ) -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

        account = Account.query.get(account_id)
        if account is None:
            raise ValueError("Счёт не найден")

        tx = Transaction(
            type=type_,
            amount=amount,
            category_id=category_id,
            account_id=account_id,
            department_id=department_id,
            counterparty_id=counterparty_id,
            description=description,
            date=tx_date or date.today(),
        )

        TransactionService._apply_to_balance(account, type_, amount)

        db.session.add(tx)
        db.session.commit()
        return tx

    @staticmethod
    def delete(transaction_id: int) -> None:
        tx = Transaction.query.get(transaction_id)
        if tx is None:
            return
        account = tx.account
        TransactionService._revert_from_balance(account, tx.type, tx.amount)
        db.session.delete(tx)
        db.session.commit()

    @staticmethod
    def _apply_to_balance(account: Account, type_: TransactionType, amount: Decimal) -> None:
        if type_ == TransactionType.INCOME:
            account.balance = (account.balance or 0) + amount
        else:
            account.balance = (account.balance or 0) - amount

    @staticmethod
    def _revert_from_balance(account: Account, type_: TransactionType, amount: Decimal) -> None:
        if type_ == TransactionType.INCOME:
            account.balance = (account.balance or 0) - amount
        else:
            account.balance = (account.balance or 0) + amount
