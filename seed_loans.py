
from datetime import datetime, timedelta

from app import app
from extensions import db
from models.models import Customer, Loan


with app.app_context():

    customer = Customer.query.first()

    if not customer:
        print("No demo customer found. Register first.")
    elif Loan.query.filter_by(customer_id=customer.id).first():
        print("Demo loans already exist. No duplicate records added.")
    else:

        today = datetime.utcnow()

        demo_loans = [

            Loan(
                loan_type="PERSONAL",
                loan_name="Personal Loan",
                principal_paise=20000000,
                outstanding_paise=15000000,
                emi_paise=850000,
                interest_rate=10.5,
                tenure_months=36,
                next_emi_date=today + timedelta(days=26),
                status="ACTIVE",
                customer_id=customer.id
            ),

            Loan(
                loan_type="HOME",
                loan_name="Home Loan",
                principal_paise=150000000,
                outstanding_paise=120000000,
                emi_paise=1400000,
                interest_rate=8.5,
                tenure_months=240,
                next_emi_date=today + timedelta(days=30),
                status="ACTIVE",
                customer_id=customer.id
            ),

            Loan(
                loan_type="VEHICLE",
                loan_name="Vehicle Loan",
                principal_paise=50000000,
                outstanding_paise=35000000,
                emi_paise=1000000,
                interest_rate=9.5,
                tenure_months=60,
                next_emi_date=today + timedelta(days=35),
                status="ACTIVE",
                customer_id=customer.id
            )

        ]

        db.session.add_all(demo_loans)
        db.session.commit()

        print("Three demo loans added successfully!")
