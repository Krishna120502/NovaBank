
from app import app
from extensions import db
from models.models import Customer, BankAccount, Transaction

with app.app_context():

    customer = Customer.query.first()

    if not customer:
        print("No registered customer found.")
    else:
        account = BankAccount.query.filter_by(
            customer_id=customer.id
        ).first()

        if not account:
            print("No bank account found.")
        else:
            demo_transactions = [
                {
                    "reference_number": "NOVA-DEMO-001",
                    "transaction_type": "CREDIT",
                    "description": "Salary Credit",
                    "amount_paise": 2500000
                },
                {
                    "reference_number": "NOVA-DEMO-002",
                    "transaction_type": "DEBIT",
                    "description": "Online Shopping",
                    "amount_paise": 250000
                },
                {
                    "reference_number": "NOVA-DEMO-003",
                    "transaction_type": "CREDIT",
                    "description": "Money Received",
                    "amount_paise": 500000
                }
            ]

            added = 0

            for item in demo_transactions:
                existing = Transaction.query.filter_by(
                    reference_number=item["reference_number"]
                ).first()

                if not existing:
                    transaction = Transaction(
                        reference_number=item["reference_number"],
                        transaction_type=item["transaction_type"],
                        description=item["description"],
                        amount_paise=item["amount_paise"],
                        status="SUCCESS",
                        account_id=account.id
                    )

                    db.session.add(transaction)
                    added += 1

            db.session.commit()

            print(f"{added} demo transactions added successfully.")

