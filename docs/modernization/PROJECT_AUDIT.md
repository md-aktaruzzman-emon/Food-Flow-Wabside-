# FoodFlow — Comprehensive Project & Architecture Audit

## 1. Executive Summary & Existing Architecture

**FoodFlow** is a Django 5 web platform designed to eliminate community food waste by connecting food donors (restaurants, grocers, households, and event caterers) with verified food recipients (shelters, charities, community kitchens, and individuals in need). The application is built with standard Django full-stack patterns: server-rendered HTML templates, vanilla JavaScript micro-interactions, Django ORM, and session-based authentication with role separation.

### Application Architecture & Apps

| Django App | Purpose & Core Responsibilities | Key Models & Business Logic |
| :--- | :--- | :--- |
| **`accounts`** | User lifecycle, custom authentication, role management, profile management, and role-specific dashboards. | `User` (AbstractUser with `is_donor`, `is_recipient`), `Donor` (profile with `donor_type`, `is_verified`), `Recipient` (profile with `recipient_type`, `is_verified`). |
| **`listings`** | Creation, updating, browsing, and media management for donated food items. | `FoodListing` (quantities, units, expiration timestamps, statuses: available, claimed, completed, expired), `FoodPhoto` (gallery images per listing, max 5). |
| **`claims`** | Reservation of surplus food by verified recipients, 8-character unique pickup token generation, atomic state transitions, and physical handover verification by donors. | `Claim` (reserved quantity, pickup deadline, unique `pickup_code`, statuses: pending, completed, cancelled, expired), `ClaimService` (thread-safe transactions using `select_for_update`). |
| **`locations`** | Physical address management with deduplication. | `Location` (address, area, city, geo-coordinates). Normalized via `get_or_create_location`. |
| **`notifications`** | In-app alerts for recipients regarding nearby food donations, claim state changes, and pickup reminders. | `Notification` (type, recipient, listing, message, unread status), `NotificationService`. |

---

## 2. Main Problems Discovered

### A. UI/UX & Design Deficiencies
1. **Severe Inline Style Fragmentation & Code Smells:**
   - Templates rely heavily on hardcoded inline CSS (`style="..."`), arbitrary hex codes (`#234432`, `#173f35`, `#294335`, `#183d2c`, `#78877a`), and inline padding/margin values.
   - The landing page (`templates/home.html`) spans 1,146 lines containing repetitive 5-step card grids, placeholder text ("Replace the URL below with your own image link"), and decorative clutter that resembles generic template stitching rather than a focused food rescue platform.
2. **Critical Responsive Layout Breakage on Profile Page:**
   - In `templates/accounts/profile.html`, the profile picture card uses `position: absolute; left: calc(100% + 24px); width: 280px;`. On any viewport narrower than ~1200px (all tablets and mobile phones), this panel is pushed completely off-screen, creating a huge horizontal scrollbar and breaking mobile navigation.
3. **No Responsive Mobile Navigation:**
   - `templates/partials/navbar.html` has no hamburger toggle, drawer, or dropdown for small viewports. On mobile screens (< 768px), navigation items either wrap awkwardly across multiple lines or overflow horizontally.
4. **Visual Hierarchy & Typography Inconsistency:**
   - Inconsistent font sizes, arbitrary letter-spacing (`letter-spacing: 2px/3px`), lack of unified heading rhythm, and competing badge colors without standardized design tokens.
5. **Form UX Gaps:**
   - No password visibility toggles on registration and login.
   - Role selection does not provide smooth visual feedback.
   - The 8-character pickup code in `claims/claim_detail.html` and `claims/my_claims.html` lacks modern visual distinction and one-click copying.

### B. Backend & Query Optimization (Django Patterns)
1. **N+1 Query Problems on Listings & Photos:**
   - `FoodListing.visible_to_recipients()` executes `select_related('donor', 'location')`. However, cards display `listing.photos.all|first` and `listing.donor.user.full_name`. Because `photos` is not prefetched and `donor__user` is not selected, browsing 20 listings triggers **20 separate photo queries** plus additional user queries.
   - In `recipient_dashboard_view` and `home_view`, listings are rendered without prefetching photos, compounding query overhead.
2. **Redundant Aggregations in `quantity_available`:**
   - `listing.quantity_available` issues a dynamic `Sum('claimed_quantity')` query on every evaluation. When listing cards evaluate both `quantity_available` and `remaining_time`, multiple queries are fired per listing.
3. **Duplicated Expiry Sweeps Across Views:**
   - Four distinct views (`donor_dashboard_view`, `donor_listings_list_view`, `recipient_dashboard_view`, `claims_list_view`) independently duplicate lazy updates:
     `FoodListing.objects.filter(..., expires_at__lte=now).update(status='expired')`
     This logic should be encapsulated inside `ExpiryService`.

### C. Security Deficiencies (Django Security)
1. **Hardcoded Secret Key Fallback:**
   - `config/settings.py` falls back to `'django-insecure-foodflow-university-cse-lab-secret-key-2026'`. In production (`DEBUG=False`), missing `SECRET_KEY` should raise a configuration error.
2. **Wildcard `ALLOWED_HOSTS` & Missing Security Headers:**
   - `ALLOWED_HOSTS = ['*']` allows Host header poisoning in production.
   - Missing HTTP security headers: `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = 'DENY'`, `SECURE_HSTS_SECONDS`, and conditional SSL redirection.
   - `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are hardcoded to `False`, allowing transmission over unencrypted connections even when HTTPS is configured.
3. **Cascade Deletion Vulnerability on Food Listings:**
   - In `listings/views.py`: `donor_listing_delete_view` does not check if active pending claims or completed claims exist. A donor deleting a listing cascades and deletes all claims made by recipients, wiping pickup audit trails.
4. **Orphaned Media Files:**
   - When a `FoodPhoto` is deleted via `donor_photo_delete_view`, only the database record is deleted; the physical image file on disk is left orphaned in `media/`.
5. **Completely Empty Password Validators:**
   - `AUTH_PASSWORD_VALIDATORS = []` in settings allows 1-character passwords. User registration should enforce minimum password complexity while maintaining compatibility with testing fixtures.

### D. Accessibility Findings (WCAG 2.2 AA)
1. **Low Contrast Text (SC 1.4.3):**
   - Muted text colors `#bedcc5` on `#173f35` (contrast ~3.1:1, failing AA), `#78877a` on `#ffffff` (contrast ~3.8:1, failing AA), and `#d5e6ca` on dark banners fail minimum 4.5:1 contrast requirements.
2. **Missing Skip to Main Content Link (SC 2.4.1):**
   - Keyboard users must tab through all navigation items on every page reload before reaching main content.
3. **Inconsistent Focus Indicators (SC 2.4.7 / 2.4.11):**
   - Inputs and interactive buttons lack high-contrast visible focus rings when navigated via keyboard.
4. **Missing ARIA Live Regions (SC 4.1.3):**
   - Live countdown timers, notification counter polls, and pickup code verifications lack `aria-live="polite"` feedback for screen reader users.
5. **No Reduced Motion Query (SC 2.3.3):**
   - Pulse animations and smooth transitions do not respect `prefers-reduced-motion: reduce`.

---

## 3. Prioritized Modernization Task List

### Critical Priority
- [x] Fix profile page layout bug (`picture-panel` absolute positioning causing viewport horizontal scroll).
- [ ] Implement responsive mobile navigation drawer with accessible hamburger toggle in `templates/partials/navbar.html`.
- [ ] Build a cohesive, modern CSS design system in `static/css/styles.css` using CSS custom properties for color, typography, spacing, elevation, and component tokens; eliminate chaotic inline styling across all templates.
- [ ] Fix N+1 queries in `listings/models.py` (`visible_to_recipients`), `browse.html`, and dashboards by selecting `donor__user` and prefetching `photos`.
- [ ] Add listing deletion safety check: prevent deletion if active pending or completed claims exist.
- [ ] Clean up production security settings (`SECRET_KEY` validation, security headers, secure cookies when not in debug mode).

### High Priority
- [ ] Redesign landing page (`templates/home.html`): clear value proposition, authentic food-sharing imagery, clear donor/recipient CTA paths, live verified metrics, remove redundant placeholder sections.
- [ ] Modernize authentication views (`login.html`, `register.html`): clean split/card layout, password visibility toggle, accessible role switcher.
- [ ] Modernize Donor and Recipient dashboards: clean stat counters, quick-action cards, responsive data tables/cards for pending pickups.
- [ ] Modernize Food Discovery (`browse.html`) & Food Details (`food_detail_recipient.html`): filter pills, live urgency countdowns, accessible quantity selector, prominent pickup location cards.
- [ ] Enhance Claims and Pickup Workflow (`my_claims.html`, `claim_detail.html`, `verify_pickup.html`): prominent 8-character token display with one-click copy, formatted pickup code input field.
- [ ] Clean up physical photo file deletion on `FoodPhoto` removal.

### Medium Priority
- [ ] Implement WCAG 2.2 AA fixes: "Skip to main content" link, accessible focus rings (`:focus-visible`), verified color contrast (>= 4.5:1), ARIA labels and live status updates.
- [ ] Centralize lazy expiry logic into `ExpiryService`.
- [ ] Add password minimum length validation in registration form.

### Low Priority
- [ ] Add empty state illustrations and helpful recovery links for zero-search results and empty notification lists.
- [ ] Respect `prefers-reduced-motion` for countdown and badge animations.
- [ ] Create comprehensive end-to-end Playwright test suite verifying donor and recipient workflows.
- [ ] Compile full test and verification reports in `docs/modernization/`.
