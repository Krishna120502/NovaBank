
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.models import DebitCard
import secrets
from datetime import datetime, timedelta


cards = Blueprint("cards", __name__)


@cards.route("/cards")
@login_required
def my_cards():

    card = DebitCard.query.filter_by(
        customer_id=current_user.id
    ).first()

    if not card:

        expiry = datetime.now() + timedelta(days=365 * 3)

        card = DebitCard(
            card_number="DEMO-" + secrets.token_hex(4).upper(),
            card_holder=current_user.full_name.upper(),
            expiry_date=expiry.strftime("%m/%y"),
            card_type="VIRTUAL DEBIT",
            status="ACTIVE",
            customer_id=current_user.id
        )

        db.session.add(card)
        db.session.commit()

    return render_template(
        "cards.html",
        card=card
    )


@cards.route("/cards/toggle-status", methods=["POST"])
@login_required
def toggle_status():

    card = DebitCard.query.filter_by(
        customer_id=current_user.id
    ).first_or_404()

    if card.status == "ACTIVE":
        card.status = "BLOCKED"
        flash("Demo card blocked successfully.", "success")
    else:
        card.status = "ACTIVE"
        flash("Demo card activated successfully.", "success")

    db.session.commit()

    return redirect(url_for("cards.my_cards"))
