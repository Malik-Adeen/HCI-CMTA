---
name: Rahbar Transit
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#3f4941'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#6f7a70'
  outline-variant: '#bec9be'
  surface-tint: '#046d3e'
  primary: '#00502c'
  on-primary: '#ffffff'
  primary-container: '#006b3c'
  on-primary-container: '#90e9ad'
  inverse-primary: '#81d99f'
  secondary: '#a63b00'
  on-secondary: '#ffffff'
  secondary-container: '#ff6f2e'
  on-secondary-container: '#5e1e00'
  tertiary: '#0b4586'
  on-tertiary: '#ffffff'
  tertiary-container: '#2f5da0'
  on-tertiary-container: '#c3d7ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
  surface-base: '#FFFFFF'
  surface-subtle: '#F7F7F7'
  error-red: '#B00020'
  success-green: '#006B3C'
  orange-line: '#D4500A'
  green-line: '#006B3C'
  blue-line: '#00529B'
typography:
  display-lg:
    fontFamily: Source Serif 4
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 60px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Source Serif 4
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
  headline-lg-mobile:
    fontFamily: Source Serif 4
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-md:
    fontFamily: Source Serif 4
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  body-lg:
    fontFamily: Source Sans 3
    fontSize: 22px
    fontWeight: '400'
    lineHeight: 32px
  body-md:
    fontFamily: Source Sans 3
    fontSize: 20px
    fontWeight: '400'
    lineHeight: 30px
  label-lg:
    fontFamily: Source Sans 3
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 24px
    letterSpacing: 0.05em
  cta:
    fontFamily: Source Sans 3
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 24px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1200px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
  touch-target-min: 56px
---

## Brand & Style

The design system is centered on the concept of "Dignified Mobility." Designed specifically for the elderly population in Pakistan, it prioritizes legibility, cognitive ease, and physical accessibility. The personality is reliable, community-oriented, and safe.

The visual style is **Corporate / Modern** with a focus on **High-Contrast** utility. It utilizes a "Clean-Utility" aesthetic: heavy whitespace to prevent cognitive overload, large-scale typography to assist those with visual impairments, and oversized interactive elements to accommodate reduced motor precision. Every design decision is guided by WCAG 2.1 AAA standards.

## Colors

The palette leverages the national identity through a deep **Primary Dark Green**, chosen for its cultural resonance and high legibility against white backgrounds. **Accent Orange** is used strictly for critical calls to action and safety warnings. **Supportive Blue** is reserved for route-specific information.

Minimum contrast ratio: 7:1 for body text, 4.5:1 for large text and UI components.

## Typography

- **Source Serif 4** — headings (authoritative, clear at large scales)
- **Source Sans 3** — body text (open counters, distinct shapes, low-vision friendly)
- **Noto Nastaliq Urdu** — Urdu language toggle
- Base body size: **20px minimum**. Line height: 1.5x. Never justify text.

## Layout & Spacing

- 12-column grid desktop, 4-column mobile
- 8px linear spacing scale
- **Minimum touch target: 56×56px** (elderly users with reduced dexterity)
- 64px+ section padding

## Key Component Rules

- Buttons: minimum 56px tall, always text-labelled (never icon-only)
- Input fields: permanent visible label above (no floating labels), minimum 60px height
- Cards: white background, 2px border, 16px corner radius, 24px internal padding
- Focus rings: 3px solid Accent Orange (#ff6f2e) on all interactive elements
- No transparency / backdrop blur — reduces contrast for aging eyes
- No justified text

## Mapping to Existing index.html CSS Vars

| Stitch token | Existing var | Value |
|---|---|---|
| primary | --green-dark | #004D2B / #00502c |
| primary-container | --green | #006B3C |
| secondary | --orange | #D4500A / #a63b00 |
| secondary-container | N/A | #ff6f2e |
| tertiary | --blue | #1A4D8F / #0b4586 |
| background | --bg | #FAFAF8 / #fcf9f8 |
| on-surface | --text-primary | #1A1A1A / #1c1b1b |
| surface-base | --bg-card | #FFFFFF |
