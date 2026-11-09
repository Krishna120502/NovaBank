
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.models import Transaction, BankAccount

transactions = Blueprint("transactions", __name__)


@transactions.route("/transactions")
@login_required
def history():

    records = (
        Transaction.query
        .join(BankAccount)
        .filter(BankAccount.customer_id == current_user.id)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

    total_credits = sum(
        t.amount_paise for t in records
        if t.transaction_type.upper() == "CREDIT"
        and t.status.upper() == "SUCCESS"
    )

    total_debits = sum(
        t.amount_paise for t in records
        if t.transaction_type.upper() == "DEBIT"
        and t.status.upper() == "SUCCESS"
    )

    total_transactions = len(records)

    return render_template(
        "transactions.html",
        transactions=records,
        total_credits=total_credits,
        total_debits=total_debits,
        total_transactions=total_transactions
    )
