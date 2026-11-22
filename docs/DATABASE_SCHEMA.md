# PARTBASE Database Schema Specification

This document outlines the entity relationships and tables within the PARTBASE data layer.

## Entity Relationship Overview

```
 [User] 1 ---- 1 [Shop] (for Employers)
   |
   +---- 1 [SeekerProfile] (for Seekers)
   |
   +---- * [Job] (via Shop)
   |       |
   |       +---- * [Application] ---- * [User] (Seeker)
   |       |
   |       +---- * [Rating] (Double-blind)
   |       |
   |       +---- * [Report] (Community grievance)
   |
   +---- * [Ticket] (Support desk)
   |
   +---- * [Payment] (₹49 listing boost)
```

## Tables & Primary Keys

1. **`users`**:
   - `id`: Integer Primary Key
   - `phone`: String(15), Unique, Indexed
   - `name`: String(100)
   - `area_id`: Foreign Key (`areas.id`)
   - `is_admin`, `is_blocked`: Boolean flags

2. **`shops`**:
   - `id`: Integer Primary Key
   - `owner_user_id`: Foreign Key (`users.id`)
   - `shop_name`, `address`: String
   - `verification_status`: Enum (`pending`, `verified`, `rejected`)

3. **`jobs`**:
   - `id`: Integer Primary Key
   - `shop_id`: Foreign Key (`shops.id`)
   - `category`: String (e.g. `shop_helper`, `packing`)
   - `pay_amount`, `pay_type`: Integer / String
   - `status`: Enum (`open`, `filled`, `hidden`, `deleted`)
   - `report_count`: Integer (Auto-hides at $\ge 3$)
   - `boosted_until`: DateTime
