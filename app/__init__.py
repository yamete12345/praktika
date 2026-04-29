from flask import Flask
from config import Config
from app.database import db


def create_app(config_class: type = Config) -> Flask:
    """Фабрика Flask-приложения."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.transactions import bp as transactions_bp
    from app.routes.categories import bp as categories_bp
    from app.routes.departments import bp as departments_bp
    from app.routes.counterparties import bp as counterparties_bp
    from app.routes.accounts import bp as accounts_bp
    from app.routes.reports import bp as reports_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(departments_bp, url_prefix="/departments")
    app.register_blueprint(counterparties_bp, url_prefix="/counterparties")
    app.register_blueprint(accounts_bp, url_prefix="/accounts")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    with app.app_context():
        db.create_all()
        from app.database import seed_initial_data
        seed_initial_data()

    return app
