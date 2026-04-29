from datetime import datetime, date
from enum import Enum

from app.database import db


class TransactionType(str, Enum):
    """Тип транзакции: доход или расход."""
    INCOME = "income"
    EXPENSE = "expense"


class CounterpartyType(str, Enum):
    """Тип контрагента: клиент или поставщик."""
    CLIENT = "client"
    SUPPLIER = "supplier"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.Enum(TransactionType), nullable=False)

    transactions = db.relationship("Transaction", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.type.value})>"


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))

    transactions = db.relationship("Transaction", back_populates="department")


class Counterparty(db.Model):
    __tablename__ = "counterparties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.Enum(CounterpartyType), nullable=False)
    inn = db.Column(db.String(20))
    contact = db.Column(db.String(150))

    transactions = db.relationship("Transaction", back_populates="counterparty")


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    balance = db.Column(db.Numeric(14, 2), nullable=False, default=0)

    transactions = db.relationship("Transaction", back_populates="account")


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    counterparty_id = db.Column(db.Integer, db.ForeignKey("counterparties.id"))

    category = db.relationship("Category", back_populates="transactions")
    account = db.relationship("Account", back_populates="transactions")
    department = db.relationship("Department", back_populates="transactions")
    counterparty = db.relationship("Counterparty", back_populates="transactions")
