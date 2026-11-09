
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from models.models import Loan, LoanPayment

loans = Blueprint("loans", __name__)


@loans.route("/loans")
@login_required
def overview():

    records = Loan.query.filter_by(
        customer_id=current_user.id
    ).order_by(Loan.created_at.desc()).all()

    total_principal = sum(
        loan.principal_paise for loan in records
    )

    total_outstanding = sum(
        loan.outstanding_paise for loan in records
    )

    total_emi = sum(
        loan.emi_paise for loan in records
        if loan.status.upper() == "ACTIVE"
    )

    active_loans = sum(
        1 for loan in records
        if loan.status.upper() == "ACTIVE"
    )

    return render_template(
        "loans.html",
        loans=records,
        total_principal=total_principal,
        total_outstanding=total_outstanding,
        total_emi=total_emi,
        active_loans=active_loans
    )


@loans.route("/loans/<int:loan_id>")
@login_required
def details(loan_id):

    loan = Loan.query.filter_by(
        id=loan_id,
        customer_id=current_user.id
    ).first_or_404()

    payments = LoanPayment.query.filter_by(
        loan_id=loan.id
    ).order_by(LoanPayment.payment_date.desc()).all()

    total_paid = sum(
        payment.amount_paise
        for payment in payments
        if payment.status.upper() == "SUCCESS"
    )

    return render_template(
        "loan_details.html",
        loan=loan,
        payments=payments,
        total_paid=total_paid
    )
