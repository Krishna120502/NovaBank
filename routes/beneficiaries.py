
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.models import Beneficiary, BankAccount

beneficiaries = Blueprint("beneficiaries", __name__)


@beneficiaries.route("/beneficiaries", methods=["GET", "POST"])
@login_required
def manage():

    if request.method == "POST":

        name = request.form.get("beneficiary_name", "").strip()
        account_number = request.form.get("account_number", "").strip()

        if not name or len(name) > 100:
            flash("Enter a valid beneficiary name.", "error")
            return redirect(url_for("beneficiaries.manage"))

        if not account_number.isdigit() or len(account_number) != 12:
            flash("Enter a valid 12-digit account number.", "error")
            return redirect(url_for("beneficiaries.manage"))

        own_account = BankAccount.query.filter_by(
            account_number=account_number,
            customer_id=current_user.id
        ).first()

        if own_account:
            flash("You cannot add your own account as a beneficiary.", "error")
            return redirect(url_for("beneficiaries.manage"))

        receiver = BankAccount.query.filter_by(
            account_number=account_number,
            status="ACTIVE"
        ).first()

        if not receiver:
            flash("NOVABANK demo account not found.", "error")
            return redirect(url_for("beneficiaries.manage"))

        existing = Beneficiary.query.filter_by(
            customer_id=current_user.id,
            account_number=account_number
        ).first()

        if existing:
            flash("This beneficiary is already saved.", "error")
            return redirect(url_for("beneficiaries.manage"))

        beneficiary = Beneficiary(
            beneficiary_name=name,
            account_number=account_number,
            customer_id=current_user.id
        )

        db.session.add(beneficiary)
        db.session.commit()

        flash("Beneficiary added successfully.", "success")

        return redirect(url_for("beneficiaries.manage"))

    saved_beneficiaries = Beneficiary.query.filter_by(
        customer_id=current_user.id
    ).order_by(Beneficiary.created_at.desc()).all()

    return render_template(
        "beneficiaries.html",
        beneficiaries=saved_beneficiaries
    )


@beneficiaries.route("/beneficiaries/delete/<int:beneficiary_id>", methods=["POST"])
@login_required
def delete(beneficiary_id):

    beneficiary = Beneficiary.query.filter_by(
        id=beneficiary_id,
        customer_id=current_user.id
    ).first_or_404()

    db.session.delete(beneficiary)
    db.session.commit()

    flash("Beneficiary deleted successfully.", "success")

    return redirect(url_for("beneficiaries.manage"))
