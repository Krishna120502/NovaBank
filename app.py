
from flask import Flask, redirect, url_for

from config import Config
from extensions import db, login_manager, csrf

from models.models import Customer, BankAccount, Transaction, Beneficiary, DebitCard, Investment, Loan, LoanPayment

from routes.auth import auth
from routes.dashboard import dashboard
from routes.transactions import transactions
from routes.transfers import transfers
from routes.beneficiaries import beneficiaries
from routes.cards import cards
from routes.investments import investments
from routes.loans import loans



def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Login settings
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."

    # Load logged-in customer
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(Customer, int(user_id))
        except (ValueError, TypeError):
            return None

    # Register routes
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(transactions)
    app.register_blueprint(transfers)
    app.register_blueprint(beneficiaries)
    app.register_blueprint(cards)
    app.register_blueprint(investments)
    app.register_blueprint(loans)

    # Home page
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
