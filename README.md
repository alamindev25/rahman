# Alrahman87 Healthcare Platform - Backend

A robust, enterprise-grade healthcare and clinic management REST API built with **Django** and **Django REST Framework (DRF)**. The platform powers healthcare service discovery, clinic registrations, dialysis appointment scheduling, subscription management, payment processing, multilingual content, and real-time push notifications.

---

## 🚀 Key Features

- **Authentication & Security:**
  - JWT-based authentication (`SimpleJWT`) with Bearer tokens & HTTP-only cookies.
  - Social authentication (Google OAuth2).
  - Secure OTP verification for signup and password reset.
  - Role-based permissions (Patients, Clinic Owners, Admins).

- **Clinic & Partner Management:**
  - Clinic profiles, verification licenses, and status approvals.
  - Treatment management, facilities, pricing, and operating shifts.
  - Reviews and rating system.

- **Appointment & Slot Scheduling:**
  - Dynamic slot capacity, shift configurations, and weekly schedules.
  - Clinic blackout date management.
  - Patient appointment bookings with payment verification.

- **Payment & Subscriptions:**
  - **Stripe** payment gateway integration.
  - Subscription plans, billing intervals, and automated webhook handling.

- **Notifications & Communication:**
  - Real-time mobile push notifications via **Firebase Cloud Messaging (FCM)**.
  - Device token tracking and multi-cast messaging.
  - Automated transactional email notifications.

- **CMS & Multilingual Content:**
  - Dynamic blog management with multilingual localization support.
  - Dynamic system settings, logos, icons, FAQs, and static content.

- **Asynchronous Processing & Admin:**
  - Asynchronous task processing & scheduled cron jobs using **Celery** & **Celery Beat**.
  - Modern, responsive admin dashboard powered by **Django Unfold**.

---

## 🛠️ Tech Stack

- **Framework:** Python 3.10+, Django 5.x, Django REST Framework
- **Authentication:** `djangorestframework-simplejwt`, Google OAuth2
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **Task Queue & Cache:** Celery, Redis
- **Cloud & Integrations:** Firebase Admin SDK, Stripe, Cloudinary, AWS S3
- **Admin Panel:** Django Unfold

---

## 📁 Project Structure

```text
alrahman87_django/
├── apps/                       # Modular Django apps
│   ├── about_us/               # About us page content & stats
│   ├── appoinment/             # Appointment scheduling & slots
│   ├── blog/                   # Blog articles & categories
│   ├── clinic/                 # Clinic registration & management
│   ├── cms/                    # Dynamic CMS & landing content
│   ├── contact/                # Contact inquiries
│   ├── dashboard/              # Analytics & admin dashboards
│   ├── language/               # Multilingual translation services
│   ├── notification/           # Device tokens & push notifications
│   ├── payment/                # Stripe transactions & webhooks
│   ├── resources/              # Patient guides & resources
│   ├── seeders/                # Initial data seeders
│   ├── social_auth/            # Google OAuth authentication
│   ├── subscription/           # Clinic subscription plans
│   ├── system_setting/         # Global site settings & assets
│   ├── user/                   # Custom user model & profile
│   └── utils/                  # Shared utilities & middlewares
├── media/                      # Uploaded media assets
├── project/                    # Project settings, URLs, WSGI/ASGI & Celery
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── firebase.py
├── static/                     # Static files (CSS, JS)
├── templates/                  # HTML templates & email formats
├── API_DOCUMENTATION.md        # Comprehensive API documentation
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── serviceAccountKey.json.example # Firebase credentials template
```

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/alamindev25/rahman.git
cd rahman
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

Key variables to configure:
- `SECRET_KEY`: Django secret key
- `DEBUG`: `True` for development, `False` for production
- `DB_ENGINE`: `sqlite` or `django.db.backends.postgresql`
- `STRIPE_SECRET_KEY` & `STRIPE_WEBHOOK_SECRET`
- `GOOGLE_CLIENT_ID` & `GOOGLE_SECRET_KEY`
- `EMAIL_HOST_USER` & `EMAIL_HOST_PASSWORD`

### 5. Setup Firebase Credentials
Copy the example service account template and supply your Firebase service account JSON:
```bash
cp serviceAccountKey.json.example serviceAccountKey.json
```

### 6. Run Migrations & Seed Data
```bash
python manage.py migrate

# Optional: seed initial dummy data
python manage.py seed
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## ⚡ Celery & Background Workers

To run Celery worker and Celery Beat scheduler for background tasks:

```bash
# Start Celery Worker
celery -A project worker --loglevel=info

# Start Celery Beat Scheduler
celery -A project beat --loglevel=info
```

---

## 📖 API Documentation

Detailed endpoint specifications, request payloads, and response examples are available in [API_DOCUMENTATION.md](file:///c:/Users/alamin/Downloads/alrahman87_django/alrahman87_django/API_DOCUMENTATION.md).

- **Base API URL:** `http://127.0.0.1:8000/api/`
- **Admin Dashboard:** `http://127.0.0.1:8000/admin/`

---

## 🔒 Security Best Practices

- Do **not** commit `.env` or `serviceAccountKey.json` to version control.
- Ensure `DEBUG=False` in production environments.
- Use strong database passwords and restrict allowed hosts in production.

---

## 📄 License
This project is proprietary and confidential. All rights reserved.
