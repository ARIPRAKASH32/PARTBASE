import re
from datetime import datetime
from app.extensions import db

def mask_phone(phone):
    """
    Mask phone number for privacy: e.g. +91 98765 43210 -> +91 98xxx xxxxx
    """
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    if len(digits) >= 10:
        country_code = "+91 " if phone.startswith("+91") else ""
        first_two = digits[-10:-8]
        return f"{country_code}{first_two}xxx xxxxx"
    return phone

def format_currency(amount, pay_type="hour"):
    """
    Format pay display: e.g. ₹120/hr or ₹600/day
    """
    suffix = "/hr" if pay_type == "hour" else "/day"
    return f"₹{amount}{suffix}"

def reveal_ratings_if_both_rated(job_id, application_id=None):
    """
    Double-blind rating reveal logic:
    Checks if both seeker_to_shop and shop_to_seeker ratings exist.
    When both have rated, sets revealed = True on both ratings,
    and updates the Shop rating average/count and Seeker rating average/jobs_completed.
    """
    from app.models import Rating, Shop, SeekerProfile, Application

    query = Rating.query.filter_by(job_id=job_id)
    if application_id:
        query = query.filter_by(application_id=application_id)
    
    ratings = query.all()
    has_seeker_rated = any(r.direction == "seeker_to_shop" for r in ratings)
    has_shop_rated = any(r.direction == "shop_to_seeker" for r in ratings)

    if has_seeker_rated and has_shop_rated:
        for r in ratings:
            r.revealed = True
        db.session.commit()

        # Update Shop ratings
        seeker_to_shop_ratings = Rating.query.filter_by(direction="seeker_to_shop", revealed=True).all()
        # Find which shop was rated
        first_rating = ratings[0]
        shop = Shop.query.filter_by(owner_user_id=first_rating.ratee_id).first() or \
               Shop.query.filter_by(owner_user_id=first_rating.rater_id).first()
        if shop:
            shop_ratings = [r.stars for r in seeker_to_shop_ratings if r.ratee_id == shop.owner_user_id]
            if shop_ratings:
                shop.rating_count = len(shop_ratings)
                shop.rating_avg = round(sum(shop_ratings) / len(shop_ratings), 1)

        # Update Seeker ratings
        seeker_profile = SeekerProfile.query.filter(
            SeekerProfile.user_id.in_([first_rating.ratee_id, first_rating.rater_id])
        ).first()
        if seeker_profile:
            shop_to_seeker_ratings = Rating.query.filter_by(
                ratee_id=seeker_profile.user_id,
                direction="shop_to_seeker",
                revealed=True
            ).all()
            if shop_to_seeker_ratings:
                stars_list = [r.stars for r in shop_to_seeker_ratings]
                seeker_profile.rating_avg = round(sum(stars_list) / len(stars_list), 1)
            # Count completed jobs
            completed_apps = Application.query.filter_by(seeker_id=seeker_profile.user_id, status="completed").count()
            seeker_profile.jobs_completed = max(seeker_profile.jobs_completed, completed_apps)

        db.session.commit()
        return True
    return False

def check_and_auto_hide_job(job_id):
    """
    Moderation Rule: If a job accumulates 3 or more reports,
    it is automatically hidden from seeker listings until reviewed by an admin.
    """
    from app.models import Job, Report
    job = Job.query.get(job_id)
    if not job:
        return False

    report_count = Report.query.filter_by(job_id=job_id).count()
    job.report_count = report_count
    if report_count >= 3:
        if job.status not in ["deleted", "hidden"]:
            job.status = "hidden"
            db.session.commit()
            return True
    db.session.commit()
    return False
