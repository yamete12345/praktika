from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import func, case

from app.database import db
from app.models import Transaction, Category, Department, TransactionType


class AnalyticsService:
    """Алгоритмы агрегации финансовых данных для отчётов."""

    @staticmethod
    def total_by_type(
        type_: TransactionType,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> Decimal:
        query = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.type == type_
        )
        query = AnalyticsService._apply_date_range(query, date_from, date_to)
        return Decimal(query.scalar() or 0)

    @staticmethod
    def profit(date_from: Optional[date] = None, date_to: Optional[date] = None) -> Decimal:
        income = AnalyticsService.total_by_type(TransactionType.INCOME, date_from, date_to)
        expense = AnalyticsService.total_by_type(TransactionType.EXPENSE, date_from, date_to)
        return income - expense

    @staticmethod
    def by_category(
        type_: TransactionType,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> list[dict]:
        query = (
            db.session.query(Category.name, func.sum(Transaction.amount))
            .join(Transaction, Transaction.category_id == Category.id)
            .filter(Transaction.type == type_)
            .group_by(Category.name)
        )
        query = AnalyticsService._apply_date_range(query, date_from, date_to)
        return [{"category": name, "total": float(total or 0)} for name, total in query.all()]

    @staticmethod
    def by_department(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> list[dict]:
        query = (
            db.session.query(
                Department.name,
                func.sum(
                    case(
                        (Transaction.type == TransactionType.INCOME, Transaction.amount),
                        else_=0,
                    )
                ),
                func.sum(
                    case(
                        (Transaction.type == TransactionType.EXPENSE, Transaction.amount),
                        else_=0,
                    )
                ),
            )
            .join(Transaction, Transaction.department_id == Department.id)
            .group_by(Department.name)
        )
        query = AnalyticsService._apply_date_range(query, date_from, date_to)
        return [
            {
                "department": name,
                "income": float(income or 0),
                "expense": float(expense or 0),
                "profit": float((income or 0) - (expense or 0)),
            }
            for name, income, expense in query.all()
        ]

    @staticmethod
    def monthly_trend(year: int) -> list[dict]:
        """Помесячная динамика доходов и расходов за год."""
        results = []
        for month in range(1, 13):
            date_from = date(year, month, 1)
            if month == 12:
                date_to = date(year, 12, 31)
            else:
                date_to = date(year, month + 1, 1)
            income = AnalyticsService.total_by_type(
                TransactionType.INCOME, date_from, date_to
            )
            expense = AnalyticsService.total_by_type(
                TransactionType.EXPENSE, date_from, date_to
            )
            results.append({
                "month": month,
                "income": float(income),
                "expense": float(expense),
            })
        return results

    @staticmethod
    def _apply_date_range(query, date_from: Optional[date], date_to: Optional[date]):
        if date_from:
            query = query.filter(Transaction.date >= date_from)
        if date_to:
            query = query.filter(Transaction.date <= date_to)
        return query
