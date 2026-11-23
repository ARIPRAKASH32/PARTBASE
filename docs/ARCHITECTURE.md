# PARTBASE System Architecture

PARTBASE is a hyper-local micro-job platform designed specifically for neighborhood retail businesses and local workers across Chennai pilot zones (OMR and Anna Nagar).

## High-Level Topology

```
                  +-----------------------------------+
                  |         Client Web Browser        |
                  |    (Desktop, Mobile, PWA App)     |
                  +-----------------+-----------------+
                                    |
                            HTTP / HTTPS (5000)
                                    |
                  +-----------------v-----------------+
                  |       Flask Application Core      |
                  |   (Session Auth, CSRF Protection) |
                  +--------+--------+--------+--------+
                           |        |        |
         +-----------------+        |        +-----------------+
         |                          |                          |
+--------v-------+         +--------v-------+         +--------v-------+
|  Auth Blueprint|         |Seeker Blueprint|         |Employer Bluepr.|
|  - OTP Auth    |         | - Shift Feed   |         | - Post Shift   |
|  - Role Switch |         | - Geo Filter   |         | - Applicants   |
|  - Demo Portals|         | - Apply Flow   |         | - ₹49 Boost    |
+----------------+         +----------------+         +----------------+
         |                          |                          |
         +-----------------+        |        +-----------------+
                           |        |        |
                  +--------v--------v--------v--------+
                  |         Admin & Support           |
                  | - Incident Report Moderation      |
                  | - Merchant Verification Status    |
                  | - Support Ticket Desk             |
                  +-----------------+-----------------+
                                    |
                        SQLAlchemy ORM (SQLite/PG)
                                    |
                  +-----------------v-----------------+
                  |         Relational Database       |
                  | - Users, Shops, Jobs, Reports     |
                  | - Applications, Ratings, Payments |
                  +-----------------------------------+
```

## Core Blueprints

| Blueprint | Route Prefix | Primary Responsibilities |
|---|---|---|
| `auth` | `/` | Phone OTP authentication, role switcher (`seeker`, `employer`, `admin`), instant demo sandboxes |
| `seeker` | `/seeker` | Local shift directory, category filtering, walking distance calculations, 1-click apply |
| `employer`| `/employer` | Shift publishing, live applicant tracker, double-blind rating submission, ₹49 listing boost |
| `admin` | `/admin` | Zero-fee policy enforcement, report queue moderation, employer verifications, audit logs |
| `support` | `/support` | Ticket submission desk, grievance tracking, user profile management |
| `api` | `/api` | REST endpoints for mobile/PWA integrations, live scam keyword validation |

## Design Principles

1. **Zero Registration Fees**: No seeker ever pays registration fees or advance security deposits.
2. **Hyper-Local Proximity**: Jobs clustered within 1–3 KM walking distance in Chennai localities.
3. **Double-Blind Reviews**: Ratings are revealed only after both seeker and merchant have reviewed each other.
