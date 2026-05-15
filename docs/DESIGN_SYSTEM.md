# Design System Reference
> Extracted from frontend/index.html — single source of truth for all UI decisions

---

## Color Palette

```css
--green:        #006B3C   /* Primary — navbar border, buttons, icons */
--green-dark:   #004D2B   /* Hero bg, info bar, hover states */
--green-light:  #E6F4EE   /* Section backgrounds, card hovers */
--orange:       #D4500A   /* CTA buttons, accent, alerts */
--orange-light: #FFF0E8   /* Orange card backgrounds */
--blue:         #1A4D8F   /* Blue line, info badges */
--blue-light:   #E8F0FB   /* Blue card backgrounds */
--gold:         #B8860B   /* Senior/special fare badges */
--text-primary:   #1A1A1A
--text-secondary: #3D3D3D
--text-muted:     #5A5A5A
--bg:           #FAFAF8   /* Page background */
--bg-card:      #FFFFFF
--border:       #D4D0C8
```

---

## Typography

```css
/* Fonts loaded */
'Source Sans 3'    → body text (weights 400, 600, 700, 800)
'Lora'             → headings / serif (weights 400, 600, 700)
'Noto Nastaliq Urdu' → Urdu language toggle

/* Font scale — ALL enlarged for elderly accessibility */
--fs-xs:   1rem       /* 16px — minimum body text */
--fs-sm:   1.125rem   /* 18px — secondary text, labels */
--fs-base: 1.25rem    /* 20px — body default */
--fs-md:   1.5rem     /* 24px — subheadings */
--fs-lg:   2rem       /* 32px — section titles */
--fs-xl:   2.75rem    /* 44px — hero subheading */
--fs-xxl:  3.5rem     /* 56px — hero H1 */
```

---

## Spacing & Radius

```css
--radius:    12px   /* Cards, buttons */
--radius-lg: 20px   /* Large cards, hero card */
--shadow:    0 4px 24px rgba(0,0,0,0.10)
--shadow-lg: 0 8px 40px rgba(0,0,0,0.14)
```

---

## Component Patterns

### Section wrapper
```html
<section class="section [section-alt | section-dark]">
  <div class="container">
    <span class="section-label">Label text</span>
    <h2 class="section-title">Section Title</h2>
    <p class="section-subtitle">Description...</p>
    <!-- content -->
  </div>
</section>
```

### Button variants
```html
<a class="btn btn-primary">Primary (orange fill)</a>
<a class="btn btn-outline">Outline (transparent, white border)</a>
```

### Quick action card
```html
<a class="quick-card">
  <div class="quick-icon qi-green">emoji</div>
  <h3>Title</h3>
  <p>Description</p>
</a>
```

### Line color headers
```css
.line-header.orange  → #D4500A to #F07030
.line-header.blue    → #1A4D8F to #2A6ACC
.line-header.green   → #006B3C to #008B4E
.line-header.red     → #B91C1C to #DC2626  /* to add */
.line-header.pink    → #9D174D to #BE185D  /* to add */
.line-header.electric → #065F46 to #059669 /* to add */
```

---

## Accessibility Rules

- Font size minimum: 16px (`--fs-xs`) — never smaller
- Focus ring: `4px solid var(--orange)` on all interactive elements
- ARIA labels on all icons, buttons, regions
- Skip link present (`.skip-link`)
- Font size controls (A+ / A−) in navbar
- High contrast: dark text on light bg everywhere
- Urdu font ready: `Noto Nastaliq Urdu` imported, needs RTL toggle (`dir="rtl"`)

---

## New Pages Checklist

Each new page must include:
- [ ] Same `<head>` block (fonts, meta, shared CSS link)
- [ ] Same info-bar
- [ ] Same navbar (with correct `.active` class on current page link)
- [ ] `<main id="main-content">` wrapper
- [ ] Same footer
- [ ] Same back-to-top button
- [ ] Same JS: nav toggle, font controls, back-to-top
- [ ] AI chat floating widget (ai-chat.js)
- [ ] PWA manifest link

---

## PWA Requirements

```html
<!-- In <head> of every page -->
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#006B3C">
<meta name="apple-mobile-web-app-capable" content="yes">
```

```json
// manifest.json
{
  "name": "Islamabad Metro — CMTA",
  "short_name": "IslamabadMetro",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#006B3C",
  "background_color": "#FAFAF8",
  "icons": [{ "src": "/static/icon-192.png", "sizes": "192x192" }]
}
```
