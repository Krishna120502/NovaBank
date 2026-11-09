
from datetime import datetime
from flask_login import UserMixin
from extensions import db


class Customer(UserMixin, db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    mobile = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    pin_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    failed_attempts = db.Column(
        db.Integer,
        default=0
    )

    locked_until = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    accounts = db.relationship(
        "BankAccount",
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class BankAccount(db.Model):

    __tablename__ = "bank_accounts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    account_number = db.Column(
        db.String(12),
        unique=True,
        nullable=False
    )

    account_type = db.Column(
        db.String(30),
        default="SAVINGS"
    )

    balance_paise = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="ACTIVE"
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    customer = db.relationship(
        "Customer",
        back_populates="accounts"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    transactions = db.relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete-orphan"
    )


class Transaction(db.Model):

    __tablename__ = "transactions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    reference_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )

    description = db.Column(
        db.String(150),
        nullable=False
    )

    amount_paise = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="SUCCESS"
    )

    transaction_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    account_id = db.Column(
        db.Integer,
        db.ForeignKey("bank_accounts.id"),
        nullable=False
    )

    account = db.relationship(
        "BankAccount",
        back_populates="transactions"
    )


class Beneficiary(db.Model):

    __tablename__ = "beneficiaries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    beneficiary_name = db.Column(
        db.String(100),
        nullable=False
    )

    account_number = db.Column(
        db.String(20),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class DebitCard(db.Model):

    __tablename__ = "debit_cards"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    card_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    card_holder = db.Column(
        db.String(100),
        nullable=False
    )

    expiry_date = db.Column(
        db.String(10),
        nullable=False
    )

    card_type = db.Column(
        db.String(30),
        default="VIRTUAL DEBIT"
    )

    status = db.Column(
        db.String(20),
        default="ACTIVE"
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class Investment(db.Model):

    __tablename__ = "investments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    investment_type = db.Column(
        db.String(50),
        nullable=False
    )

    investment_name = db.Column(
        db.String(100),
        nullable=False
    )

    invested_amount_paise = db.Column(
        db.Integer,
        nullable=False
    )

    expected_return_rate = db.Column(
        db.Float,
        default=0
    )

    investment_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    maturity_date = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="ACTIVE"
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

class Loan(db.Model):

    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)

    loan_type = db.Column(db.String(50), nullable=False)
    loan_name = db.Column(db.String(100), nullable=False)

    principal_paise = db.Column(db.Integer, nullable=False)
    outstanding_paise = db.Column(db.Integer, nullable=False)
    emi_paise = db.Column(db.Integer, nullable=False)

    interest_rate = db.Column(db.Float, default=0)
    tenure_months = db.Column(db.Integer, nullable=False)

    next_emi_date = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.String(20), default="ACTIVE")

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoanPayment(db.Model):

    __tablename__ = "loan_payments"

    id = db.Column(db.Integer, primary_key=True)

    loan_id = db.Column(
        db.Integer,
        db.ForeignKey("loans.id"),
        nullable=False
    )

    amount_paise = db.Column(db.Integer, nullable=False)

    payment_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    reference_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="SUCCESS"
    )
