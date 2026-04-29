from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def seed_initial_data() -> None:
    """Наполняет БД начальными справочниками, если они пусты."""
    from app.models import Category, Account, Department, TransactionType

    if Category.query.count() == 0:
        defaults = [
            Category(name="Продажи", type=TransactionType.INCOME),
            Category(name="Услуги", type=TransactionType.INCOME),
            Category(name="Зарплата", type=TransactionType.EXPENSE),
            Category(name="Аренда", type=TransactionType.EXPENSE),
            Category(name="Налоги", type=TransactionType.EXPENSE),
            Category(name="Закупка материалов", type=TransactionType.EXPENSE),
        ]
        db.session.add_all(defaults)

    if Account.query.count() == 0:
        db.session.add_all([
            Account(name="Касса", balance=0),
            Account(name="Расчётный счёт", balance=0),
        ])

    if Department.query.count() == 0:
        db.session.add_all([
            Department(name="Администрация"),
            Department(name="Производство"),
            Department(name="Продажи"),
        ])

    db.session.commit()
