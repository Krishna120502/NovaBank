
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash
)
from flask_login import login_required, current_user
from decimal import Decimal, InvalidOperation
import secrets

from extensions import db
from models.models import BankAccount, Transaction, Beneficiary

transfers = Blueprint("transfers", __name__)


@transfers.route("/transfer", methods=["GET", "POST"])
@login_required
def money_transfer():

    sender = BankAccount.query.filter_by(
        customer_id=current_user.id,
        status="ACTIVE"
    ).first()

    if not sender:
        flash("No active account found.", "error")
        return redirect(url_for("dashboard.home"))

    # Get only the logged-in customer's beneficiaries
    saved_beneficiaries = Beneficiary.query.filter_by(
        customer_id=current_user.id
    ).order_by(Beneficiary.beneficiary_name.asc()).all()

    if request.method == "POST":

        beneficiary_id = request.form.get(
            "beneficiary_id", ""
        ).strip()

        receiver_number = request.form.get(
            "account_number", ""
        ).strip()

        # Use the selected saved beneficiary
        if beneficiary_id:

            if not beneficiary_id.isdigit():
                flash("Invalid beneficiary selection.", "error")
                return redirect(url_for("transfers.money_transfer"))

            selected_beneficiary = Beneficiary.query.filter_by(
                id=int(beneficiary_id),
                customer_id=current_user.id
            ).first()

            if not selected_beneficiary:
                flash("Selected beneficiary was not found.", "error")
                return redirect(url_for("transfers.money_transfer"))

            receiver_number = selected_beneficiary.account_number

        # Otherwise, use manually entered account number
        if not receiver_number or not receiver_number.isdigit():
            flash("Enter a valid beneficiary account number.", "error")
            return redirect(url_for("transfers.money_transfer"))

        amount_input = request.form.get(
            "amount", ""
        ).strip()

        description = request.form.get(
            "description", "Money Transfer"
        ).strip()

        try:
            amount = Decimal(amount_input)

            if not amount.is_finite() or amount <= 0:
                raise InvalidOperation

            amount_paise_decimal = amount * 100

            if amount_paise_decimal != amount_paise_decimal.to_integral_value():
                raise InvalidOperation

            amount_paise = int(amount_paise_decimal)

        except (InvalidOperation, ValueError):
            flash(
                "Enter a valid transfer amount with up to 2 decimal places.",
                "error"
            )
            return redirect(url_for("transfers.money_transfer"))

        if amount_paise < 100:
            flash("Minimum transfer amount is ₹1.", "error")
            return redirect(url_for("transfers.money_transfer"))

        if amount_paise > 100000000:
            flash(
                "Maximum demo transfer amount is ₹10,00,000.",
                "error"
            )
            return redirect(url_for("transfers.money_transfer"))

        if len(description) > 150:
            flash(
                "Description must be 150 characters or less.",
                "error"
            )
            return redirect(url_for("transfers.money_transfer"))

        receiver = BankAccount.query.filter_by(
            account_number=receiver_number,
            status="ACTIVE"
        ).first()

        if not receiver:
            flash(
                "Beneficiary account not found or inactive.",
                "error"
            )
            return redirect(url_for("transfers.money_transfer"))

        if receiver.id == sender.id:
            flash(
                "You cannot transfer money to your own account.",
                "error"
            )
            return redirect(url_for("transfers.money_transfer"))

        if sender.balance_paise < amount_paise:
            flash(
                "Insufficient demo account balance.",
                "error"
            )
            return redirect(url_for("transfers.money_transfer"))

        try:
            sender.balance_paise -= amount_paise
            receiver.balance_paise += amount_paise

            transfer_id = secrets.token_hex(6).upper()

            debit_transaction = Transaction(
                reference_number="NOVA-" + transfer_id + "-D",
                transaction_type="DEBIT",
                description=description or "Money Transfer",
                amount_paise=amount_paise,
                status="SUCCESS",
                account_id=sender.id
            )

            credit_transaction = Transaction(
                reference_number="NOVA-" + transfer_id + "-C",
                transaction_type="CREDIT",
                description="Received: " + (
                    description or "Money Transfer"
                ),
                amount_paise=amount_paise,
                status="SUCCESS",
                account_id=receiver.id
            )

            db.session.add(debit_transaction)
            db.session.add(credit_transaction)

            db.session.commit()

            flash(
                "Demo transfer completed successfully!",
                "success"
            )

            return redirect(url_for("transactions.history"))

        except Exception:
            db.session.rollback()

            flash(
                "Transfer could not be completed. Please try again.",
                "error"
            )

    return render_template(
        "transfer.html",
        account=sender,
        beneficiaries=saved_beneficiaries
    )
