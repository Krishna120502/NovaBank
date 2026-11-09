
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets

from extensions import db
from models.models import Customer, BankAccount

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("full_name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        pin = request.form.get("pin", "")
        confirm_pin = request.form.get("confirm_pin", "")

        if not name or len(name) > 100:
            flash("Please enter a valid full name.", "error")
            return redirect(url_for("auth.register"))

        if not mobile.isdigit() or len(mobile) != 10 or mobile[0] not in "6789":
            flash("Enter a valid 10-digit Indian mobile number.", "error")
            return redirect(url_for("auth.register"))

        if not pin.isdigit() or len(pin) != 4:
            flash("MPIN must contain exactly 4 digits.", "error")
            return redirect(url_for("auth.register"))

        if pin != confirm_pin:
            flash("MPIN entries do not match.", "error")
            return redirect(url_for("auth.register"))

        existing = Customer.query.filter_by(mobile=mobile).first()

        if existing:
            flash("This mobile number is already registered.", "error")
            return redirect(url_for("auth.register"))

        customer = Customer(
            full_name=name,
            mobile=mobile,
            pin_hash=generate_password_hash(pin)
        )

        db.session.add(customer)
        db.session.flush()

        account = BankAccount(
            account_number=str(secrets.randbelow(900000000000) + 100000000000),
            account_type="SAVINGS",
            balance_paise=0,
            customer_id=customer.id
        )

        db.session.add(account)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        mobile = request.form.get("mobile", "").strip()
        pin = request.form.get("pin", "")

        customer = Customer.query.filter_by(mobile=mobile).first()

        if not customer:
            flash("Invalid mobile number or MPIN.", "error")
            return redirect(url_for("auth.login"))

        now = datetime.utcnow()

        if customer.locked_until and customer.locked_until > now:
            flash("Account temporarily locked. Please try again later.", "error")
            return redirect(url_for("auth.login"))

        if customer.locked_until and customer.locked_until <= now:
            customer.failed_attempts = 0
            customer.locked_until = None

        if check_password_hash(customer.pin_hash, pin):

            customer.failed_attempts = 0
            customer.locked_until = None

            db.session.commit()

            login_user(customer)

            return redirect(url_for("dashboard.home"))

        customer.failed_attempts = (customer.failed_attempts or 0) + 1

        if customer.failed_attempts >= 5:
            customer.locked_until = now + timedelta(minutes=15)
            flash("Too many incorrect attempts. Try again after 15 minutes.", "error")
        else:
            flash("Invalid mobile number or MPIN.", "error")

        db.session.commit()

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have logged out successfully.", "success")

    return redirect(url_for("auth.login"))
