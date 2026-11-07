<div align="center">

  <img src="static/images/logo.svg" alt="Food-Flow Logo" width="64" height="64" />

  <h1>Food-Flow</h1>

  <img
    src="docs/assets/readme/food-flow-banner.gif"
    alt="Food-Flow — Animated 3D food donation and sharing scene: Good Food Deserves a Second Destination"
    width="100%"
  />

  <p><strong>Share More Food. Waste Less. Build a Better Community.</strong></p>

  <p>
    An expiry-aware, community-driven food donation and surplus rescue platform connecting restaurants, grocers, and households with verified shelters, charities, and individuals before wholesome food expires.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12%2B-174B38?style=flat-square&logo=python&logoColor=white" alt="Python 3.12+" />
    <img src="https://img.shields.io/badge/Django-5.2.18-092E20?style=flat-square&logo=django&logoColor=white" alt="Django 5.2.18" />
    <img src="https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-3D805B?style=flat-square&logo=postgresql&logoColor=white" alt="Database: SQLite | PostgreSQL" />
    <img src="https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20ES6-E99B52?style=flat-square&logo=javascript&logoColor=white" alt="Frontend: HTML5 | CSS3 | Vanilla JS" />
    <img src="https://img.shields.io/badge/Static%20Assets-WhiteNoise%206.12-26332D?style=flat-square" alt="WhiteNoise 6.12" />
    <img src="https://img.shields.io/badge/Imaging-Pillow%2012.3-A9C4A9?style=flat-square" alt="Pillow 12.3" />
  </p>

  <p>
    <a href="#about-food-flow">About</a> •
    <a href="#key-features">Key Features</a> •
    <a href="#screenshots-and-interface-preview">Interface Preview</a> •
    <a href="#how-food-flow-works">Workflows</a> •
    <a href="#project-architecture">Architecture</a> •
    <a href="#installation-and-setup">Setup Guide</a> •
    <a href="#security">Security</a>
  </p>

</div>

---

## Table of Contents

1. [About Food-Flow](#about-food-flow)
2. [Brand Identity and Visual Direction](#brand-identity-and-visual-direction)
3. [Key Features](#key-features)
4. [Screenshots and Interface Preview](#screenshots-and-interface-preview)
5. [How Food-Flow Works](#how-food-flow-works)
6. [Technology Stack](#technology-stack)
7. [Project Architecture](#project-architecture)
8. [Installation and Setup](#installation-and-setup)
9. [Environment Variables](#environment-variables)
10. [Database](#database)
11. [Testing](#testing)
12. [Security](#security)
13. [Deployment](#deployment)
14. [Roadmap](#roadmap)
15. [Contributing](#contributing)
16. [License](#license)
17. [Credits and Contact](#credits-and-contact)

---

## About Food-Flow

**Food-Flow** is a full-stack web application built with Django to solve a critical urban and community coordination problem: **edible surplus food is routinely discarded because donors lack a structured, time-sensitive channel to reach local recipients before the food spoils.**

Restaurants, bakeries, grocers, and households often have surplus prepared meals or fresh produce at the end of a service window. At the same time, neighborhood shelters, non-profit organizations, and families face barriers discovering what is available nearby, how many portions remain, when the food expires, and how to coordinate a reliable pickup.

Food-Flow bridges this gap through an **expiry-aware rescue workflow**:

- **Time-Bounded Listings:** Every donation requires an explicit expiration timestamp (enforced between 30 minutes and 72 hours ahead). Live countdown timers track remaining shelf life, and automated sweeps transition expired listings out of circulation.
- **Portion-Accurate Reservations:** Recipients can claim the full quantity or reserve partial portions (such as 5 out of 20 meal boxes), immediately updating real-time availability for other community members.
- **Accountable Physical Handover:** Every claim generates a unique **8-character alphanumeric pickup token** paired with a 90-minute pickup window. Donors verify this token on-site to confirm physical collection and complete the rescue record.
- **Neighborhood Matching:** When a donor posts surplus food, the platform automatically notifies verified recipients in the same city and municipal area.

---

## Brand Identity and Visual Direction

Food-Flow is designed around the central creative thesis: **"Good Food Deserves a Second Destination."** Rather than adopting a clinical or corporate aesthetic, the interface pairs organic forest greens and warm parchment surfaces with high-contrast editorial typography and clear status indicators.

| Color Role | Hex Value | Visual Application |
| :--- | :--- | :--- |
| **Deep Forest Green** | `#174B38` | Primary brand anchors, hero containers, donor workspace banners |
| **Fresh Green** | `#3D805B` | Interactive primary buttons, active status badges, verified indicators |
| **Soft Sage** | `#A9C4A9` | Subtle borders, secondary badges, calm ambient accents |
| **Warm Cream** | `#F7F4EA` | Primary page canvas and accessible reading surfaces |
| **Natural Orange** | `#E99B52` | Urgency indicators, countdown highlights, recipient callouts |
| **Dark Charcoal** | `#26332D` | High-contrast body typography and structural headings |

The 3D hero banner (`docs/assets/readme/food-flow-banner.gif`) illustrates this identity in motion: fresh produce and artisan bread move from woven donor baskets on the left, travel across an arched timber-and-emerald bridge inside a donation crate, and arrive at a warm community sharing table with prepared bowls and packaged meals on the right.

---

## Key Features

### Implemented Platform Capabilities

- **Role-Based Authentication & Profiles (`accounts`)**
  - Custom `User` model (`AUTH_USER_MODEL = 'accounts.User'`) supporting distinct **Donor** (`restaurant`, `grocery`, `bakery`, `hotel`, `catering`, `individual`) and **Recipient** (`charity`, `shelter`, `community`, `individual`) roles.
  - Dedicated registration flows that simultaneously provision user credentials, role profiles, and normalized location records.
  - Profile management with validated avatar uploads (JPEG, PNG, WebP up to 5 MB) and automatic vector fallback (`default-avatar.svg`).

- **Surplus Food Listing & Photo Management (`listings`)**
  - Donors can create, edit, and delete food listings with portion quantities (`DecimalField`), measurement units (`kg`, `portions`, `plates`, `boxes`, `packets`, `liters`, `items`), descriptions, and pickup addresses.
  - Multi-photo gallery support (`FoodPhoto` model) with captioning, PIL magic-byte image validation, UUID-randomized storage paths, and an interactive client-side lightbox (`gallery.js`).
  - Automatic vector illustration fallback (`default-food.svg`) when a listing is posted without photographs.

- **Expiry-Aware Inventory & Automated Sweeps (`listings` & `claims`)**
  - Real-time client-side countdown timers (`countdown.js`) on every listing card and detail page.
  - Server-side `ExpiryService` and custom management command (`python manage.py expiry_sweep`) that automatically mark past-deadline listings and unclaimed reservations as `expired` and restore uncollected inventory back to `available`.

- **Food Discovery, Search & Area Filtering (`listings` & `locations`)**
  - Recipients browse active, non-expired donations sorted by urgency (`expires_at`).
  - Keyword search across food names and descriptions combined with dynamic City and Area filtering.
  - Database-annotated remaining quantity calculation (`quantity_available`) that prevents N+1 query bottlenecks.

- **Partial & Full Claim Management (`claims`)**
  - Concurrency-safe claim creation (`ClaimService.create_claim`) using database row locking (`select_for_update()`) inside atomic transactions.
  - Automatic 90-minute pickup deadline assignment (`PICKUP_WINDOW_MINUTES = 90`).
  - Recipient claim cancellation workflow that safely returns reserved portions to the active listing pool if the listing has not yet expired.

- **8-Character Token Pickup Verification (`claims`)**
  - Cryptographically generated 8-character uppercase alphanumeric `pickup_code` assigned to each reservation.
  - Dedicated Donor Pickup Verification Terminal (`/donor/pickups/verify/`) with sliding-window rate limiting and donor-scoped lookup protection.
  - Instant state transition to `completed` upon valid token entry, recording `completed_at` timestamps and automatically closing the parent listing once all portions are collected.

- **Location-Matched In-App Notifications (`notifications`)**
  - `LocationMatchingService` identifies recipients in the donor's city and area when new surplus food is posted.
  - Lifecycle alerts for recipients when a new listing is available nearby, when a pickup code isverified, or when a reservation expires.
  - Background polling endpoint (`/notifications/unread-count/`) coupled with `notifications.js` to update the navbar unread badge in real time.

---

## Screenshots and Interface Preview

All screenshots below are captured directly from the running Food-Flow application.

### 1. Public Landing Page & Live Impact Metrics
The homepage introduces the platform mission, live database metrics (active donations, completed rescues, verified donors), workflow overview, and recent surplus listings.

<div align="center">
  <img src="docs/assets/readme/screenshots/01-homepage.png" alt="Food-Flow Homepage" width="100%" />
</div>

---

### 2. Food Discovery & Expiry-Aware Directory
Recipients browse available surplus food with keyword search, city/area filters, remaining portion counters, and live expiration countdowns.

<div align="center">
  <img src="docs/assets/readme/screenshots/02-food-discovery.png" alt="Food Discovery and Browse Page" width="100%" />
</div>

---

### 3. Food Listing Details & Portion Reservation
Detailed view displaying donor verification status, pickup address, remaining quantity, countdown timer, and the portion claim form.

<div align="center">
  <img src="docs/assets/readme/screenshots/03-food-details.png" alt="Food Listing Details and Claim Form" width="100%" />
</div>

---

### 4. Donor Workspace & Pending Handover Queue
Donors monitor active listings, pending recipient pickups, completed rescues, and incoming reservations awaiting on-site token verification.

<div align="center">
  <img src="docs/assets/readme/screenshots/04-donor-dashboard.png" alt="Donor Dashboard" width="100%" />
</div>

---

### 5. Recipient Workspace & Active Pickup Tokens
Recipients track their active reservations, pickup deadlines, 8-character verification codes, and nearby available donations.

<div align="center">
  <img src="docs/assets/readme/screenshots/05-recipient-dashboard.png" alt="Recipient Dashboard" width="100%" />
</div>

---

### 6. Pickup Verification Terminal & Claim Management

| Donor Pickup Verification Terminal | Recipient Claims & Token History |
| :---: | :---: |
| <img src="docs/assets/readme/screenshots/06-pickup-verification.png" alt="Donor Pickup Verification Terminal" width="100%" /> | <img src="docs/assets/readme/screenshots/07-recipient-claims.png" alt="Recipient Claims List" width="100%" /> |

---

### 7. Authentication Interface
Clean, accessible sign-in interface supporting username or email authentication with role-based dashboard routing.

<div align="center">
  <img src="docs/assets/readme/screenshots/08-login.png" alt="Food-Flow Sign In Page" width="85%" />
</div>

---

## How Food-Flow Works

```mermaid
flowchart LR
    subgraph Donor["1. Donor Workflow"]
        D1["Register / Log In"] --> D2["Post Surplus Listing & Photos"]
        D2 --> D3["Set Quantity & Expiry Deadline"]
    end

    subgraph Engine["2. Food-Flow Core Engine"]
        E1["Match Area & Notify Recipients"]
        E2["Track Live Portion Inventory"]
        E3["Generate 8-Char Pickup Token"]
    end

    subgraph Recipient["3. Recipient Workflow"]
        R1["Browse & Filter Local Food"] --> R2["Reserve Needed Portions"]
        R2 --> R3["Present Pickup Token On-Site"]
    end

    D3 --> E1
    E1 --> R1
    R2 --> E2
    E2 --> E3
    E3 --> R3
    R3 --> V["4. Donor Verifies Token & Completes Rescue"]
```

### Donor Step-by-Step Workflow

1. **Register or Log In:** Create an account selecting the **Food Donor** role along with organization type (restaurant, bakery, grocery, etc.) and primary address.
2. **Create a Food Listing:** Navigate to **+ Donate Food** (`/donor/listings/create/`) and enter the food name, description, total quantity, measurement unit, and expiration timestamp.
3. **Upload Photographs:** Attach an initial food photo during creation or manage multiple photos via the listing photo manager (`/donor/listings/<id>/photos/`).
4. **Automatic Community Alerting:** Upon creation, Food-Flow makes the listing discoverable and dispatches in-app notifications to recipients in the matching city and area.
5. **Review Incoming Claims:** Monitor active reservations, claimant details, reserved quantities, and pickup deadlines from the Donor Dashboard (`/donor/dashboard/`).
6. **Verify Physical Pickup:** When the recipient arrives on-site, open the **Verify Pickup** terminal (`/donor/pickups/verify/`) and enter their 8-character pickup code.
7. **Complete Handover:** Submitting a valid code marks the claim as `Completed`, updates community rescue totals, and transitions the listing to `Completed` once all portions are fulfilled.

### Recipient Step-by-Step Workflow

1. **Register or Log In:** Create an account selecting the **Food Recipient** role (charity/NGO, shelter, community group, or individual) with local area details.
2. **Receive Area Alerts:** Check the navbar notification bell or `/notifications/` feed for new surplus donations posted nearby.
3. **Discover & Filter Food:** Open **Browse Food** (`/recipient/food/`) and filter listings by keyword, city, or neighborhood area.
4. **Inspect Listing Details:** Review the donor's organization name, remaining quantity, pickup address, and real-time expiration countdown.
5. **Submit a Portion Claim:** Enter the exact quantity needed (up to the available amount) and confirm the reservation.
6. **Track Claim & Pickup Token:** Receive a unique **8-character pickup code** and a 90-minute pickup deadline on the Claim Detail page (`/claims/<id>/`) and Recipient Dashboard.
7. **Collect Food On-Site:** Arrive at the donor's pickup location before the deadline and present the 8-character token to complete the handover (or cancel the reservation online if plans change).

---

## Technology Stack

All versions below are verified directly against `requirements.txt` and `config/settings.py`:

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Language** | Python | `3.12+` (verified on `3.14.6`) | Core application runtime and business services |
| **Web Framework** | Django | `5.2.18` | ORM, authentication, routing, templates, forms, and security middleware |
| **Database (Default)** | SQLite 3 | Built-in (`db.sqlite3`) | Zero-configuration relational database for local development |
| **Database (Production)** | PostgreSQL (`psycopg2-binary` & `dj-database-url`) | `2.9.13` / `3.1.2` | Persistent relational database support via `DATABASE_URL` |
| **Image Processing** | Pillow | `12.3.0` | Image upload verification, format validation, and media handling |
| **Static Asset Serving** | WhiteNoise | `6.12.0` | Compressed static file serving (`CompressedStaticFilesStorage`) |
| **Frontend Markup** | Semantic HTML5 & Django Templates | Native | Accessible, landmark-structured server-rendered views |
| **Styling System** | Custom CSS3 (`static/css/styles.css`) | Native | Custom design tokens, responsive grids, cards, and mobile drawer |
| **Client Interactivity** | Vanilla JavaScript (ES6) | Native | Live expiry countdowns, photo lightbox, claim confirmation, notification polling |

---

## Project Architecture

```text
Food-Flow/
├── accounts/                   # Custom User model, Donor/Recipient profiles, auth views & forms
│   ├── management/commands/    # seed_foodflow_demo.py for populating demo users & listings
│   ├── migrations/             # Schema migrations (0001 through 0005)
│   ├── models.py               # User, Donor, and Recipient models
│   ├── views.py                # Login, registration, profile, and role dashboards
│   └── tests.py                # Unit tests for authentication and profile workflows
├── claims/                     # Reservation lifecycle, portion accounting, and token verification
│   ├── migrations/             # Schema & composite index migrations (0001 through 0005)
│   ├── models.py               # Claim model & 8-character pickup_code generator
│   ├── services.py             # ClaimService (atomic claiming, cancellation, token verification)
│   ├── views.py                # Recipient claim views & Donor pickup verification terminal
│   └── tests.py                # Unit tests for claim state machine and quantity rules
├── config/                     # Project-level configuration and root routing
│   ├── settings.py             # Environment-driven Django settings and security guards
│   ├── urls.py                 # Root URL dispatcher & homepage view
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
├── docs/                       # Documentation assets
│   └── assets/readme/          # 3D animated banner, static preview, and interface screenshots
├── listings/                   # Surplus food listings, multi-photo uploads, and expiry sweeps
│   ├── management/commands/    # expiry_sweep.py for scheduled expiration cleanup
│   ├── migrations/             # Schema & index migrations (0001 through 0006)
│   ├── models.py               # FoodListing and FoodPhoto models
│   ├── services.py             # ExpiryService for deadline enforcement
│   ├── views.py                # Donor CRUD views, photo manager, and recipient browse views
│   └── tests.py                # Unit tests for listing visibility and expiry logic
├── locations/                  # Normalized municipal addresses and area matching
│   ├── models.py               # Location model with concurrency-safe get_or_create_location
│   ├── services.py             # LocationMatchingService for area/city recipient discovery
│   └── tests.py                # Unit tests for location matching rules
├── notifications/              # In-app recipient notification feed and unread badge API
│   ├── models.py               # Notification model with recipient/read composite index
│   ├── services.py             # NotificationService for new listing, pickup, and expiry alerts
│   ├── views.py                # Notification list, mark-as-read, and JSON unread count endpoint
│   └── tests.py                # Unit tests for notification isolation and unread counts
├── static/                     # Source static assets
│   ├── css/styles.css          # Complete Food-Flow design system stylesheet
│   ├── images/                 # Brand logo, favicon, SVG fallbacks, and curated photography
│   └── js/                     # claims.js, countdown.js, gallery.js, notifications.js
├── templates/                  # 24 modular Django HTML templates
│   ├── accounts/               # login, register, profile, donor_dashboard, recipient_dashboard
│   ├── claims/                 # my_claims, claim_detail, verify_pickup
│   ├── listings/               # browse, food_detail_recipient, listing_detail_donor, forms, gallery
│   ├── notifications/          # notification_list
│   ├── partials/               # navbar, footer, messages
│   ├── base.html               # Master layout shell
│   └── home.html               # Public landing page
├── .env.example                # Documented environment variable template
├── manage.py                   # Django CLI entry point
└── requirements.txt            # Pinned Python dependencies
```

---

## Installation and Setup

Follow these steps in **Windows PowerShell** to run Food-Flow locally.

### 1. Prerequisites

- **Python:** Version `3.12` or newer installed and added to your `PATH`.
- **Git:** Installed for cloning the repository.

### 2. Clone the Repository

```powershell
git clone https://github.com/md-aktaruzzman-emon/Food-Flow-Wabside-.git
cd Food-Flow-Wabside-
```

### 3. Create and Activate a Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **Note:** If PowerShell blocks script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first, then re-run `.\venv\Scripts\Activate.ps1`.

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure Environment Variables (Optional for Local Dev)

For local development, Food-Flow works out of the box with sensible defaults. To customize local settings, copy the example template:

```powershell
Copy-Item .env.example .env
```

### 6. Apply Database Migrations

```powershell
python manage.py migrate
```

### 7. Load Sample Demo Data (Optional)

Food-Flow includes an idempotent management command that populates sample verified donors, recipients, active food listings, claims, and notifications:

```powershell
python manage.py seed_foodflow_demo
```

### 8. Create an Administrator Account (Optional)

```powershell
python manage.py createsuperuser
```

### 9. Collect Static Files and Start the Development Server

```powershell
python manage.py collectstatic --noinput
python manage.py runserver
```

Open your browser and visit:

- **Main Application:** `http://127.0.0.1:8000/`
- **Django Admin Panel:** `http://127.0.0.1:8000/admin/`

---

## Environment Variables

All environment variables below are read directly by `config/settings.py` and documented in `.env.example`:

| Variable | Purpose | Required | Default (Local Dev) |
| :--- | :--- | :---: | :--- |
| `DEBUG` | Enables debug mode (`True` for local dev, must be `False` in production) | No | `True` |
| `SECRET_KEY` | Cryptographic signing key for sessions and CSRF tokens | **Yes (in Prod)** | Local dev fallback key |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames/domains | No | `*` (when `DEBUG=True`) |
| `DATABASE_URL` | PostgreSQL connection string (`postgres://user:pass@host:port/db`) | **Yes (on Vercel Prod)** | Uses local `db.sqlite3` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted origins (`https://...`) | No | Localhost & Vercel defaults |
| `DJANGO_SESSION_ENGINE` | Session storage backend | No | `django.contrib.sessions.backends.db` |
| `SECURE_SSL_REDIRECT` | Redirect HTTP traffic to HTTPS when `DEBUG=False` | No | `True` (when `DEBUG=False`) |
| `SECURE_HSTS_SECONDS` | HTTP Strict Transport Security duration in seconds | No | `31536000` (1 year) |
| `SERVE_MEDIA_IN_PROD` | Serve uploaded media via Django when no reverse proxy is present | No | `False` |
| `EMAIL_BACKEND` | Django email backend class | No | `django.core.mail.backends.console.EmailBackend` |
| `DEFAULT_FROM_EMAIL` | Default sender email address for system notifications | No | `no-reply@foodflow.local` |
| `EMAIL_HOST` | SMTP server hostname | No | `localhost` |
| `EMAIL_PORT` | SMTP server port | No | `587` |
| `EMAIL_USE_TLS` | Enable TLS encryption for SMTP connections | No | `True` |
| `EMAIL_HOST_USER` | SMTP authentication username | No | Empty string |
| `EMAIL_HOST_PASSWORD` | SMTP authentication password / API key | No | Empty string |

---

## Database

### Local Development (`SQLite 3`)
By default, when `DATABASE_URL` is not set in the environment, Food-Flow uses a local SQLite database at `BASE_DIR / 'db.sqlite3'`. All schema definitions and composite performance indexes are managed through standard Django migrations across `accounts`, `locations`, `listings`, `claims`, and `notifications`.

### Production (`PostgreSQL`)
When `DATABASE_URL` is provided in the environment, `config/settings.py` parses it via `dj_database_url.parse()` with persistent connection pooling (`conn_max_age=600`) and connection health checks (`conn_health_checks=True`).

### Scheduled Expiration Maintenance
To ensure expired listings and unclaimed reservations are swept even when no user visits a specific listing page, run the built-in management command periodically (e.g., every 15–30 minutes via cron or Windows Task Scheduler):

```powershell
python manage.py expiry_sweep
```

---

## Testing

Food-Flow includes **38 unit and integration tests** built with Django's native `TestCase` framework covering all 5 core domain apps:

- **`accounts/tests.py` (10 tests):** User creation, donor and recipient registration flows, password hashing, role properties, login/logout session handling, and duplicate email/username validation.
- **`claims/tests.py` (15 tests):** Full and partial portion claiming, quantity boundary enforcement, recipient cancellation and inventory restoration, pickup code verification, and unauthorized donor rejection.
- **`listings/tests.py` (5 tests):** Listing creation defaults, `visible_to_recipients()` expiry filtering, `ExpiryService` state transitions, and `FoodListingForm` deadline validation.
- **`locations/tests.py` (6 tests):** Location creation, case-insensitive normalization, area-level recipient matching, and city-level fallback matching.
- **`notifications/tests.py` (2 tests):** Notification creation, recipient feed isolation, and the `/notifications/unread-count/` JSON endpoint.

### Running the Test Suite

```powershell
python manage.py test
```

To run system and migration consistency checks:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```

---

## Security

Food-Flow implements defense-in-depth safeguards verified in the current source code:

- **Production Secret Key Enforcement:** `config/settings.py` raises `ImproperlyConfigured` if `DEBUG=False` and `SECRET_KEY` is missing or left set to the development default.
- **OWASP Password Validation:** Enforces `UserAttributeSimilarityValidator`, `MinimumLengthValidator` (8+ characters), `CommonPasswordValidator`, and `NumericPasswordValidator` on registration.
- **CSRF & POST-Only State Mutations:** All state-changing endpoints (registration, listing CRUD, claiming, cancellation, token verification, notification updates, and `/logout/`) require `POST` requests with valid CSRF tokens.
- **Tamper-Resistant Sessions:** Uses database-backed sessions (`django.contrib.sessions.backends.db`) with `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'`, and automatic `SESSION_COOKIE_SECURE = True` when `DEBUG=False`.
- **Validated Media Uploads:** Uploaded food photographs and profile avatars are verified using Pillow's `Image.open().verify()`, restricted to allowed MIME types (`JPEG`, `PNG`, `WebP`) and size limits (5 MB), and stored under UUID-randomized file paths (`food_photo_upload_path`, `user_avatar_path`) to prevent path traversal and filename collisions.
- **Scoped & Rate-Limited Pickup Verification:** Pickup token lookups are strictly scoped to the authenticated donor's own listings with unified error responses and session-based sliding-window rate limiting (maximum 10 attempts per 5 minutes) to prevent token enumeration.
- **Referential Integrity Protection:** `Claim.listing` and `Claim.recipient` foreign keys use `on_delete=models.PROTECT` to prevent accidental cascading deletion of historical rescue records.

---

## Deployment

When deploying Food-Flow to a production environment (such as a Linux VPS, Render, Railway, Fly.io, or Vercel with external PostgreSQL):

1. **Set `DEBUG=False` and a strong `SECRET_KEY`** in your environment variables.
2. **Configure a Persistent Database (`DATABASE_URL`):** Connect to a managed PostgreSQL instance. On serverless platforms like Vercel, `config/settings.py` explicitly blocks running in production (`DEBUG=False`) without `DATABASE_URL` so data is never silently written to ephemeral `/tmp` storage.
3. **Static Files:** Run `python manage.py collectstatic --noinput` during the build step. WhiteNoise (`CompressedStaticFilesStorage`) serves static assets automatically.
4. **Media Uploads (`MEDIA_ROOT`):** In single-server or container deployments, mount a persistent volume to `/media/` (and optionally set `SERVE_MEDIA_IN_PROD=True` if not using Nginx). For multi-instance or serverless deployments, configure an external S3-compatible storage backend.
5. **HTTPS & Security Headers:** When `DEBUG=False`, Django automatically enables `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` (1 year with subdomains and preload), `X_FRAME_OPTIONS = 'DENY'`, and `SECURE_CONTENT_TYPE_NOSNIFF = True`.
6. **Scheduled Expiry Sweep:** Configure a cron job or platform scheduler to execute `python manage.py expiry_sweep` every 15 minutes.

---

## Roadmap

The following enhancements represent planned future evolutions beyond the current implementation:

- **Cloud Object Storage Integration:** Native `django-storages` support for Amazon S3 / Cloudflare R2 media uploads in serverless deployments.
- **External Email & SMS Alerts:** Dispatching transactional emails and SMS notifications alongside in-app notifications when urgent surplus food is posted nearby.
- **Interactive Map Discovery:** Integrating Leaflet / OpenStreetMap coordinates on the Browse Food page for visual distance sorting.
- **Multi-Language Localization:** Adding Bengali (`bn`) and English (`en`) translation catalogs using Django's internationalization framework.

---

## Contributing

Contributions that improve food rescue workflows, accessibility, or performance are welcome:

1. Fork the repository and create a feature branch (`git checkout -b feature/your-feature-name`).
2. Make your changes following the existing app boundaries (`models.py` for data, `services.py` for business logic, `views.py` for request handling).
3. Verify that all checks and tests pass (`python manage.py check` and `python manage.py test`).
4. Commit your changes with a clear description and open a Pull Request against the `main` branch.

---

## License

No `LICENSE` file has been specified in this repository yet. Until an open-source license is formally added by the repository owner, standard copyright applies.

---

## Credits and Contact

- **Project:** Food-Flow — Expiry-Aware Food Donation & Community Rescue Platform
- **Author / Maintainer:** [Md Aktaruzzman Emon](https://github.com/md-aktaruzzman-emon)
- **Repository:** [github.com/md-aktaruzzman-emon/Food-Flow-Wabside-](https://github.com/md-aktaruzzman-emon/Food-Flow-Wabside-)
