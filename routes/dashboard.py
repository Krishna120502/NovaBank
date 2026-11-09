
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.models import BankAccount

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def home():

    accounts = BankAccount.query.filter_by(
        customer_id=current_user.id
    ).all()

    total_balance_paise = sum(
        account.balance_paise for account in accounts
    )

    return render_template(
        "dashboard.html",
        accounts=accounts,
        total_balance_paise=total_balance_paise
    )
