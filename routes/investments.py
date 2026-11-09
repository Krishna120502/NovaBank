
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

from extensions import db
from models.models import Investment

investments = Blueprint("investments", __name__)


@investments.route("/investments", methods=["GET", "POST"])
@login_required
def overview():

    if request.method == "POST":

        investment_type = request.form.get("investment_type", "").strip()
        amount_input = request.form.get("amount", "").strip()

        if investment_type not in ["FIXED DEPOSIT", "MUTUAL FUND"]:
            flash("Please select a valid investment type.", "error")
            return redirect(url_for("investments.overview"))

        try:
            amount = Decimal(amount_input)

            if not amount.is_finite() or amount <= 0:
                raise InvalidOperation

            amount_paise = int(amount * 100)

            if Decimal(amount_paise) != amount * 100:
                raise InvalidOperation

        except (InvalidOperation, ValueError):
            flash("Enter a valid investment amount.", "error")
            return redirect(url_for("investments.overview"))

        if amount_paise < 100000 or amount_paise > 100000000:
            flash("Investment must be between ₹1,000 and ₹10,00,000.", "error")
            return redirect(url_for("investments.overview"))

        if investment_type == "FIXED DEPOSIT":
            rate = 7.0
            name = "NOVABANK Demo Fixed Deposit"
            maturity = datetime.utcnow() + timedelta(days=365)
        else:
            rate = 10.0
            name = "NOVABANK Demo Mutual Fund"
            maturity = None

        record = Investment(
            investment_type=investment_type,
            investment_name=name,
            invested_amount_paise=amount_paise,
            expected_return_rate=rate,
            investment_date=datetime.utcnow(),
            maturity_date=maturity,
            status="ACTIVE",
            customer_id=current_user.id
        )

        db.session.add(record)
        db.session.commit()

        flash("Demo investment created successfully.", "success")
        return redirect(url_for("investments.overview"))

    records = Investment.query.filter_by(
        customer_id=current_user.id
    ).order_by(Investment.investment_date.desc()).all()

    total = sum(item.invested_amount_paise for item in records)

    return render_template(
        "investments.html",
        investments=records,
        total_invested_paise=total
    )
