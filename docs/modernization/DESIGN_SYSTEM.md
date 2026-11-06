# FoodFlow Design System Specification

## 1. Design Vision & Philosophy

**FoodFlow** is a community-driven, expiry-aware food donation platform. The design system is crafted to communicate **nourishment, community warmth, urgent freshness, trust, and zero-waste stewardship**.

### Anti-Generic Design Principles:
1. **Restraint Over Clutter:** No generic AI SaaS gradients, no purple-to-cyan glows, no decorative blur blobs, no floating cards inside cards.
2. **Warmth & Natural Nourishment:** Surfaces use warm bone and linen undertones (`#faf8f5`, `#f4f0e6`) rather than sterile blue-greys or muddy yellows. The brand greens are deep forest emerald (`#065f46`, `#047857`) paired with fresh mint accents (`#10b981`) and warm terracotta/amber tones (`#b45309`) for expiry urgency.
3. **Clarity & Task Speed First:** Every screen answers: *"What food is available?"*, *"Where is it?"*, *"When does it expire?"*, and *"How do I claim or hand it over?"*.
4. **Built-in WCAG 2.2 AA Conformance:** All text-to-background combinations meet or exceed 4.5:1 contrast; all interactive controls feature explicit `:focus-visible` outlines; and touch targets maintain a minimum 44×44px hit area.

---

## 2. Color Palette & Semantic Tokens

### Color Tokens (CSS Variables)

```css
:root {
  /* Brand Primary (Deep Emerald & Sage) */
  --color-primary-900: #064e3b;
  --color-primary-800: #065f46;
  --color-primary-700: #047857;
  --color-primary-600: #059669;
  --color-primary-500: #10b981;
  --color-primary-100: #d1fae5;
  --color-primary-50:  #ecfdf5;

  /* Accent Earth / Nourishment (Amber & Terracotta) */
  --color-accent-800:  #92400e;
  --color-accent-700:  #b45309;
  --color-accent-600:  #d97706;
  --color-accent-500:  #f59e0b;
  --color-accent-100:  #fef3c7;
  --color-accent-50:   #fffbeb;

  /* Neutral Ramps (Warm Stone & Ink) */
  --color-ink-900:     #111827;  /* High contrast primary text */
  --color-ink-800:     #1f2937;  /* Headings & bold elements */
  --color-ink-700:     #374151;  /* Body text (4.5:1 on light) */
  --color-ink-500:     #525f69;  /* Accessible secondary text */
  --color-ink-400:     #6b7280;  /* Muted metadata */
  
  --color-surface-bg:  #faf8f5;  /* Warm page background */
  --color-surface-card:#ffffff;  /* Card surface */
  --color-surface-sub: #f3efe8;  /* Secondary surface / table header */
  --color-border-sub:  #f0ece3;  /* Subtle divider */
  --color-border-main: #e2ddd3;  /* Input & card borders */
  --color-border-focus:#047857;  /* Focus ring outline */

  /* Semantic Feedback */
  --color-success-bg:  #ecfdf5;
  --color-success-text:#065f46;
  --color-success-border:#a7f3d0;

  --color-warning-bg:  #fffbeb;
  --color-warning-text:#92400e;
  --color-warning-border:#fde68a;

  --color-danger-bg:   #fef2f2;
  --color-danger-text: #991b1b;
  --color-danger-border:#fecaca;
  --color-danger-main: #dc2626;

  /* Focus indicator token */
  --focus-ring: 0 0 0 3px rgba(4, 120, 87, 0.35);
  --focus-ring-danger: 0 0 0 3px rgba(220, 38, 38, 0.35);
}
```

---

## 3. Typography System

The platform utilizes a system-first humanist sans font stack designed for high legibility across mobile and desktop displays without layout shifting or external font dependencies:

```css
--font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
--font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
```

### Scale & Hierarchy
| Level | Font Size | Line Height | Weight | Letter Spacing | Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display / Hero** | `clamp(2rem, 4vw, 3rem)` | 1.15 | 800 | -0.025em | Main hero headline |
| **Heading 1 (`h1`)** | `clamp(1.75rem, 3vw, 2.25rem)` | 1.25 | 700 | -0.02em | Dashboard & page headers |
| **Heading 2 (`h2`)** | `clamp(1.35rem, 2.5vw, 1.75rem)` | 1.3 | 700 | -0.015em | Major section headers |
| **Heading 3 (`h3`)** | `1.15rem` | 1.4 | 600 | -0.01em | Listing card titles, form sections |
| **Heading 4 (`h4`)** | `1.0rem` | 1.45 | 600 | 0 | Sub-panel titles, metadata groups |
| **Body Large** | `1.125rem` (18px) | 1.6 | 400 / 500 | 0 | Hero lead text, prominent descriptions |
| **Body Regular** | `1.0rem` (16px) | 1.6 | 400 | 0 | Default body text, forms, table content |
| **Body Small** | `0.875rem` (14px) | 1.5 | 400 / 500 | 0.01em | Form labels, helper text, card meta |
| **Caption / Badge** | `0.75rem` (12px) | 1.4 | 700 | 0.05em | Uppercase badges, kicker text |
| **Code / Token** | `1.5rem` | 1.0 | 700 | 0.25em | 8-character pickup verification token |

---

## 4. Spacing & Elevation

### Spacing Scale
- `2xs`: `4px`
- `xs`: `8px`
- `sm`: `12px`
- `md`: `16px`
- `lg`: `24px`
- `xl`: `32px`
- `2xl`: `48px`
- `3xl`: `64px`

### Elevation & Depth
- **Level 1 (Card default):** `box-shadow: 0 1px 3px rgba(18, 38, 28, 0.06), 0 1px 2px rgba(18, 38, 28, 0.04); border: 1px solid var(--color-border-main);`
- **Level 2 (Hover / Floating Card):** `box-shadow: 0 4px 12px rgba(18, 38, 28, 0.08), 0 1px 3px rgba(18, 38, 28, 0.05); transform: translateY(-2px);`
- **Level 3 (Modal / Nav Drawer):** `box-shadow: 0 16px 36px -6px rgba(18, 38, 28, 0.16);`

---

## 5. Core Components Specification

1. **Navbar:**
   - Sticky top with backdrop-filter blur (`background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(8px)`).
   - Brand logo with readable text mark.
   - Distinct role navigation (Donor, Recipient, Guest).
   - Unread notification count badge with `aria-live`.
   - Accessible hamburger button (`aria-expanded`, `aria-label="Toggle navigation"`) with responsive mobile off-canvas drawer.
2. **Buttons:**
   - `.btn`: Base styles with accessible touch target (>= 44px height).
   - `.btn-primary`: Solid deep emerald background (`#047857`), white text, hover darken (`#065f46`).
   - `.btn-secondary`: Warm cream stone button (`#f3efe8`), ink text (`#1f2937`), border `#e2ddd3`.
   - `.btn-outline`: Transparent surface with emerald border.
   - `.btn-danger`: Crimson warning button (`#dc2626`).
   - `.btn-sm`, `.btn-lg`: Proportionate size variants.
3. **Form Controls:**
   - Inputs, selects, and textareas share identical padding (`0.75rem 1rem`), rounded corners (`8px`), and accessible border (`#d1d5db`).
   - `:focus-visible`: 3px emerald ring with 2px offset.
   - Integrated `.form-error` messages with semantic red border and clear inline explanations.
   - Password input with clean visibility toggle button (`Show/Hide`).
4. **Food Listing Cards:**
   - Controlled 16:10 or 4:3 aspect ratio photo container with `object-fit: cover`.
   - Fallback SVG placeholder when no photo is provided.
   - Top status badges with semantic colors (Available: green, Claimed: amber, Expired: red, Completed: grey).
   - Dynamic live countdown badge with urgency threshold styling:
     - > 6 hours remaining: Sage/emerald calm pill.
     - 2–6 hours remaining: Amber warning pill.
     - < 2 hours remaining: Crimson urgent pill with subtle pulse.
     - Expired: Disabled state.
   - Clear quantity remaining progress bar and location metadata.
5. **Pickup Code Card (`pickup-code-box`):**
   - High-contrast verification card featuring the 8-character token in monospace uppercase font (`font-size: 1.75rem; letter-spacing: 0.25em`).
   - One-click "Copy Code" action with instant visual confirmation ("Copied!").
6. **Responsive Layouts:**
   - Breakpoints:
     - Mobile: `< 640px` (Single column, full-width actions, mobile nav drawer)
     - Tablet: `640px – 1024px` (2 columns, side-by-side forms)
     - Desktop: `> 1024px` (3-column food grids, multi-column dashboard statistics)
