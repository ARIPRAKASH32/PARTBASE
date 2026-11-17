import re
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from app.extensions import db
from app.models import User, Area, Job, OTPRequest
from app.services.otp_service import OTPService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def landing():
    # If already logged in, redirect to active role home
    if session.get("user_id"):
        role = session.get("role", "seeker")
        if role == "employer":
            return redirect(url_for("employer.posts"))
        return redirect(url_for("seeker.jobs"))

    # Sample jobs for landing preview
    sample_jobs = Job.query.filter_by(status="open").limit(2).all()
    return render_template("landing.html", sample_jobs=sample_jobs)

@auth_bp.route("/select-role/<role>")
def select_role(role):
    if role in ["seeker", "employer"]:
        session["intent_role"] = role
        session["role"] = role
    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        role = session.get("role", "seeker")
        return redirect(url_for("employer.posts") if role == "employer" else url_for("seeker.jobs"))

    intent_role = session.get("intent_role", "seeker")

    if request.method == "POST":
        raw_phone = request.form.get("phone", "").strip()
        cleaned_phone = re.sub(r"[^0-9+]", "", raw_phone)
        if not cleaned_phone.startswith("+"):
            cleaned_phone = "+91" + cleaned_phone.lstrip("0")

        if len(cleaned_phone) < 12:
            flash("Please enter a valid 10-digit mobile number.", "danger")
            return render_template("auth/login.html", role=intent_role, phone=raw_phone)

        provider = current_app.config.get("OTP_PROVIDER", "console")
        res = OTPService.send_otp(cleaned_phone, provider_name=provider)

        if not res["ok"]:
            flash(res["message"], "danger")
            return render_template("auth/login.html", role=intent_role, phone=raw_phone)

        session["auth_phone"] = cleaned_phone
        session["role"] = intent_role
        flash("OTP sent to your mobile number.", "success")
        return redirect(url_for("auth.verify"))

    return render_template("auth/login.html", role=intent_role)

@auth_bp.route("/verify", methods=["GET", "POST"])
def verify():
    phone = session.get("auth_phone")
    if not phone:
        flash("Please enter your mobile number first.", "warning")
        return redirect(url_for("auth.login"))

    role = session.get("role", "seeker")

    if request.method == "POST":
        # Combine OTP digits (from 6 boxes or single input)
        digits = [request.form.get(f"otp_{i}", "") for i in range(1, 7)]
        code = "".join(digits).strip() or request.form.get("otp_code", "").strip()

        if len(code) != 6 or not code.isdigit():
            flash("Please enter all 6 digits of the OTP.", "danger")
            return render_template("auth/verify.html", phone=phone, role=role)

        res = OTPService.verify_otp(phone, code)
        if not res["ok"]:
            flash(res["message"], "danger")
            return render_template("auth/verify.html", phone=phone, role=role)

        user = User.query.get(res["user_id"])
        session["user_id"] = user.id
        session["phone"] = user.phone
        session["is_admin"] = user.is_admin or (user.phone in current_app.config.get("ADMIN_PHONES", []))
        session["role"] = role
        user.active_role = role
        db.session.commit()

        # Route first-time vs returning
        if role == "seeker":
            if not user.seeker_profile or not user.name:
                return redirect(url_for("seeker.setup"))
            return redirect(url_for("seeker.jobs"))
        else:
            if not user.shop or not user.shop.shop_name:
                return redirect(url_for("employer.setup"))
            return redirect(url_for("employer.posts"))

    return render_template("auth/verify.html", phone=phone, role=role)

@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    phone = session.get("auth_phone")
    if not phone:
        return jsonify({"ok": False, "message": "Session expired. Please start over."}), 400

    provider = current_app.config.get("OTP_PROVIDER", "console")
    res = OTPService.send_otp(phone, provider_name=provider)
    return jsonify(res)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.landing"))

@auth_bp.route("/terms")
def terms():
    return render_template("landing.html", show_modal="terms")

@auth_bp.route("/privacy")
def privacy():
    return render_template("landing.html", show_modal="privacy")
