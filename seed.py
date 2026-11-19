import os
from datetime import datetime, timedelta, timezone
from app import create_app
from app.extensions import db
from app.models import User, Area, Shop, SeekerProfile, Job, Application, Rating, Report, Ticket, Payment, Draft

app = create_app()

def seed_database():
    with app.app_context():
        print("Clearing and rebuilding database...")
        db.drop_all()
        db.create_all()

        print("1. Seeding Areas in Chennai (OMR & Anna Nagar pilots)...")
        areas_data = [
            {"name": "OMR", "pincode": "600096", "lat": 12.9352, "lng": 80.2290},
            {"name": "Thoraipakkam", "pincode": "600097", "lat": 12.9431, "lng": 80.2376},
            {"name": "Neelankarai", "pincode": "600115", "lat": 12.9492, "lng": 80.2543},
            {"name": "Sholinganallur", "pincode": "600119", "lat": 12.8996, "lng": 80.2279},
            {"name": "Navalur", "pincode": "600130", "lat": 12.8458, "lng": 80.2265},
            {"name": "Perungudi", "pincode": "600096", "lat": 12.9654, "lng": 80.2461},
            {"name": "Anna Nagar", "pincode": "600040", "lat": 13.0850, "lng": 80.2101},
            {"name": "Mogappair", "pincode": "600037", "lat": 13.0837, "lng": 80.1748},
            {"name": "Shenoy Nagar", "pincode": "600030", "lat": 13.0784, "lng": 80.2248},
            {"name": "Kilpauk", "pincode": "600010", "lat": 13.0827, "lng": 80.2407}
        ]
        areas = {}
        for a_data in areas_data:
            area = Area(**a_data)
            db.session.add(area)
            db.session.flush()
            areas[a_data["name"]] = area

        print("2. Seeding Users (Admin, Employers, Seekers)...")
        # Admin user
        admin_phone = "+919876500000"
        admin_user = User(
            phone=admin_phone,
            name="LocalVelai Admin",
            area_id=areas["Anna Nagar"].id,
            is_phone_verified=True,
            active_role="admin",
            is_admin=True
        )
        db.session.add(admin_user)

        # Employers
        # Employer 1: Murugan (Sri Murugan Tailors - Verified)
        user_murugan = User(
            phone="+919876543210",
            name="Murugan",
            area_id=areas["Thoraipakkam"].id,
            lat=12.9431,
            lng=80.2376,
            is_phone_verified=True,
            active_role="employer"
        )
        db.session.add(user_murugan)
        db.session.flush()
        shop_murugan = Shop(
            owner_user_id=user_murugan.id,
            shop_name="Sri Murugan Tailors",
            owner_name="Murugan",
            address="No. 14, OMR Main Road, Thoraipakkam, Chennai",
            area_id=areas["Thoraipakkam"].id,
            lat=12.9431,
            lng=80.2376,
            verification_status="verified",
            proof_type="maps_link",
            proof_value="https://maps.google.com/?q=Sri+Murugan+Tailors+Thoraipakkam",
            rating_avg=4.6,
            rating_count=12
        )
        db.session.add(shop_murugan)

        # Employer 2: Anand (Anand Stores - Verified)
        user_anand = User(
            phone="+919876543211",
            name="Anand",
            area_id=areas["Thoraipakkam"].id,
            lat=12.9440,
            lng=80.2380,
            is_phone_verified=True,
            active_role="employer"
        )
        db.session.add(user_anand)
        db.session.flush()
        shop_anand = Shop(
            owner_user_id=user_anand.id,
            shop_name="Anand Stores",
            owner_name="Anand",
            address="2nd Cross St, Anand Nagar, Thoraipakkam, Chennai",
            area_id=areas["Thoraipakkam"].id,
            lat=12.9440,
            lng=80.2380,
            verification_status="verified",
            rating_avg=4.7,
            rating_count=8
        )
        db.session.add(shop_anand)

        # Employer 3: Meena R (Meena Fancy Store - Pending)
        user_meena = User(
            phone="+919876543212",
            name="Meena R",
            area_id=areas["Neelankarai"].id,
            lat=12.9492,
            lng=80.2543,
            is_phone_verified=True,
            active_role="employer"
        )
        db.session.add(user_meena)
        db.session.flush()
        shop_meena = Shop(
            owner_user_id=user_meena.id,
            shop_name="Meena Fancy Store",
            owner_name="Meena R",
            address="East Coast Road, Neelankarai, Chennai",
            area_id=areas["Neelankarai"].id,
            lat=12.9492,
            lng=80.2543,
            verification_status="pending",
            proof_type="maps_link",
            proof_value="https://maps.google.com/?q=Meena+Fancy+Store+Neelankarai"
        )
        db.session.add(shop_meena)

        # Employer 4: Karthik S (Tech Print Hub - Pending)
        user_karthik = User(
            phone="+919876543213",
            name="Karthik S",
            area_id=areas["Anna Nagar"].id,
            lat=13.0850,
            lng=80.2101,
            is_phone_verified=True,
            active_role="employer"
        )
        db.session.add(user_karthik)
        db.session.flush()
        shop_karthik = Shop(
            owner_user_id=user_karthik.id,
            shop_name="Tech Print Hub",
            owner_name="Karthik S",
            address="2nd Avenue, Anna Nagar, Chennai",
            area_id=areas["Anna Nagar"].id,
            lat=13.0850,
            lng=80.2101,
            verification_status="pending",
            proof_type="photo",
            proof_value="shop_front_photo.jpg"
        )
        db.session.add(shop_karthik)

        # Employer 5: Bright Tutorials
        user_bright = User(
            phone="+919876543214",
            name="Bright Admin",
            area_id=areas["OMR"].id,
            is_phone_verified=True,
            active_role="employer"
        )
        db.session.add(user_bright)
        db.session.flush()
        shop_bright = Shop(
            owner_user_id=user_bright.id,
            shop_name="Bright Tutorials",
            owner_name="Ramesh",
            address="OMR Junction, Chennai",
            area_id=areas["OMR"].id,
            verification_status="verified"
        )
        db.session.add(shop_bright)

        # Seekers
        # Seeker 1: Priya K
        user_priya = User(
            phone="+919876511111",
            name="Priya K",
            area_id=areas["OMR"].id,
            lat=12.9352,
            lng=80.2290,
            is_phone_verified=True,
            active_role="seeker",
            free_slots="weekday_evening,weekend"
        )
        db.session.add(user_priya)
        db.session.flush()
        profile_priya = SeekerProfile(
            user_id=user_priya.id,
            interests="shop_helper,packing",
            free_slots="weekday_evening,weekend",
            rating_avg=4.8,
            jobs_completed=3
        )
        db.session.add(profile_priya)

        # Seeker 2: Arun S
        user_arun = User(
            phone="+919876522222",
            name="Arun S",
            area_id=areas["OMR"].id,
            lat=12.9360,
            lng=80.2310,
            is_phone_verified=True,
            active_role="seeker",
            free_slots="weekend"
        )
        db.session.add(user_arun)
        db.session.flush()
        profile_arun = SeekerProfile(
            user_id=user_arun.id,
            interests="tutoring,delivery",
            free_slots="weekend",
            rating_avg=4.5,
            jobs_completed=1
        )
        db.session.add(profile_arun)

        # Seeker 3: Divya M
        user_divya = User(
            phone="+919876533333",
            name="Divya M",
            area_id=areas["OMR"].id,
            lat=12.9370,
            lng=80.2320,
            is_phone_verified=True,
            active_role="seeker",
            free_slots="anytime"
        )
        db.session.add(user_divya)
        db.session.flush()
        profile_divya = SeekerProfile(
            user_id=user_divya.id,
            interests="shop_helper,data_entry",
            free_slots="anytime",
            rating_avg=4.7,
            jobs_completed=2
        )
        db.session.add(profile_divya)

        db.session.commit()

        print("3. Seeding Jobs...")
        # Job 1: Shop helper at Sri Murugan Tailors (Verified, 2 needed)
        job1 = Job(
            shop_id=shop_murugan.id,
            category="shop_helper",
            title="Shop helper",
            day_option="today",
            time_range="5:00 pm to 9:00 pm",
            pay_amount=120,
            pay_type="hour",
            people_needed=2,
            hired_count=1,
            details="Light counter and stitching help. Bring your own lunch.",
            status="open",
            view_count=48
        )
        db.session.add(job1)

        # Job 2: Packing helper at Anand Stores (Urgent Boosted!)
        job2 = Job(
            shop_id=shop_anand.id,
            category="packing",
            title="Packing helper",
            day_option="today",
            time_range="Full day",
            pay_amount=600,
            pay_type="day",
            people_needed=2,
            hired_count=2,
            details="Packing grocery bags and sorting orders for fast dispatch.",
            status="open",
            is_boosted=True,
            boost_expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=24),
            view_count=35
        )
        db.session.add(job2)

        # Job 3: Shop helper at Meena Fancy Store
        job3 = Job(
            shop_id=shop_meena.id,
            category="shop_helper",
            title="Shop helper",
            day_option="today",
            time_range="4:00 pm to 8:00 pm",
            pay_amount=100,
            pay_type="hour",
            people_needed=1,
            hired_count=0,
            details="Assist with customer gift wrapping and counter billing.",
            status="open",
            view_count=19
        )
        db.session.add(job3)

        # Job 4: Tutoring at Bright Tutorials
        job4 = Job(
            shop_id=shop_bright.id,
            category="tutoring",
            title="Tutoring",
            day_option="today",
            time_range="Mon · 6:00 pm",
            pay_amount=250,
            pay_type="hour",
            people_needed=1,
            status="open"
        )
        db.session.add(job4)

        # Job 5: Data entry at Tech Print Hub
        job5 = Job(
            shop_id=shop_karthik.id,
            category="data_entry",
            title="Data entry",
            day_option="weekend",
            time_range="Sun · 10:00 am to 4:00 pm",
            pay_amount=300,
            pay_type="day",
            people_needed=1,
            status="open"
        )
        db.session.add(job5)

        # Job 6: Scam job (Hidden after 4 reports)
        job6 = Job(
            shop_id=shop_karthik.id,
            category="data_entry",
            title="Free typing job",
            day_option="today",
            pay_amount=500,
            pay_type="day",
            people_needed=5,
            details="Work from home typing job. Pay registration fee Rs 200 before you join. Easy work.",
            status="hidden",
            report_count=4,
            scam_flag=True
        )
        db.session.add(job6)

        # Job 7: Second scam job (Hidden after 3 reports)
        job7 = Job(
            shop_id=shop_meena.id,
            category="data_entry",
            title="Data entry, home",
            day_option="today",
            pay_amount=600,
            pay_type="day",
            people_needed=3,
            details="Earn Rs 1000 daily. Advance security deposit Rs 300 refundable.",
            status="hidden",
            report_count=3,
            scam_flag=True
        )
        db.session.add(job7)

        db.session.commit()

        print("4. Seeding Applications & Ratings...")
        # Priya K application on Job 1 (Hired)
        app1 = Application(
            job_id=job1.id,
            seeker_id=user_priya.id,
            note="I can come at 5 pm and have experience with stitching.",
            status="hired"
        )
        db.session.add(app1)

        # Arun S application on Job 1 (Shortlisted)
        app2 = Application(
            job_id=job1.id,
            seeker_id=user_arun.id,
            note="Available from 5 pm onwards.",
            status="shortlisted"
        )
        db.session.add(app2)

        # Divya M application on Job 1 (Applied)
        app3 = Application(
            job_id=job1.id,
            seeker_id=user_divya.id,
            note="Interested in this role.",
            status="applied"
        )
        db.session.add(app3)

        # Applications for Priya on Tutoring & Data Entry
        app4 = Application(job_id=job4.id, seeker_id=user_priya.id, status="shortlisted")
        app5 = Application(job_id=job5.id, seeker_id=user_priya.id, status="applied")
        db.session.add_all([app4, app5])

        db.session.commit()

        print("5. Seeding Reports & Support Tickets (T-1 to T-4)...")
        # Ticket T-1: Scam fee request on Free typing job (Priya)
        t1 = Ticket(
            raised_by_id=user_priya.id,
            role="seeker",
            issue_type="scam_fee_request",
            job_id=job6.id,
            description="The employer asked me to pay money before starting work.",
            status="open"
        )
        db.session.add(t1)
        db.session.flush()
        report1 = Report(
            job_id=job6.id,
            reporter_id=user_priya.id,
            reason="asked_money",
            details="Asked for Rs 200 registration fee via UPI.",
            ticket_id=t1.id
        )
        db.session.add(report1)

        # Additional reports on Job 6
        db.session.add_all([
            Report(job_id=job6.id, reporter_id=user_arun.id, reason="asked_money", details="Asked for deposit before sending PDF files.", ticket_id=t1.id),
            Report(job_id=job6.id, reporter_id=user_divya.id, reason="asked_money", details="Demanded payment before work.", ticket_id=t1.id),
            Report(job_id=job6.id, reporter_id=user_priya.id, reason="fake_shop", details="No physical shop at address.", ticket_id=t1.id)
        ])

        # Ticket T-2: Fake applicant on Packing (Anand)
        t2 = Ticket(
            raised_by_id=user_anand.id,
            role="employer",
            issue_type="fake_applicant",
            job_id=job2.id,
            description="Applicant did not match the profile.",
            status="in_review"
        )
        db.session.add(t2)

        # Ticket T-3: Wrong pay shown (Arun)
        t3 = Ticket(
            raised_by_id=user_arun.id,
            role="seeker",
            issue_type="wrong_pay",
            job_id=job1.id,
            description="The employer offered lower hourly pay than the listed amount.",
            status="in_review"
        )
        db.session.add(t3)

        # Ticket T-4: Boost payment failed (Murugan - Resolved)
        t4 = Ticket(
            raised_by_id=user_murugan.id,
            role="employer",
            issue_type="boost_payment_failed",
            job_id=job1.id,
            description="Boost payment debited but Urgent tag did not show immediately.",
            status="resolved",
            admin_reply="Resolved. Urgent boost tag reactivated for 24 hours."
        )
        db.session.add(t4)

        db.session.commit()
        print("Database successfully seeded with Chennai pilot data!")

if __name__ == "__main__":
    seed_database()
