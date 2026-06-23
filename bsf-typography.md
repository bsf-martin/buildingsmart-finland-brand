# buildingSMART Finland — Typography Specification

## Typefaces

| Role | Family | Source |
|------|--------|--------|
| Display / Headings / UI | Figtree | Google Fonts |
| Body / Long-form | Source Serif 4 | Google Fonts |
| Technical / Code | JetBrains Mono | Google Fonts |

**Google Fonts import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');
```

---

## Type scale

| Token | Size | Weight | Family | Usage |
|-------|------|--------|--------|-------|
| display | 48px | 700 | Figtree | Hero headlines only — one per page |
| h1 | 32px | 700 | Figtree | Page title — one per page |
| h2 | 24px | 600 | Figtree | Section heading |
| h3 | 18px | 600 | Figtree | Sub-section heading |
| body | 16px | 400 | Source Serif 4 | Running body text, paragraphs |
| small | 14px | 400 | Source Serif 4 | Captions, metadata, footnotes |
| label | 12px | 600 | Figtree | UI labels — uppercase, tracking 0.06em |
| mono | 13px | 400 | JetBrains Mono | Code, file types, schema names |

---

## CSS tokens

```css
:root {
  /* Families */
  --ff-display: 'Figtree', sans-serif;
  --ff-body:    'Source Serif 4', Georgia, serif;
  --ff-mono:    'JetBrains Mono', monospace;

  /* Scale */
  --fs-display: 3rem;       /* 48px */
  --fs-h1:      2rem;       /* 32px */
  --fs-h2:      1.5rem;     /* 24px */
  --fs-h3:      1.125rem;   /* 18px */
  --fs-body:    1rem;       /* 16px */
  --fs-small:   0.875rem;   /* 14px */
  --fs-label:   0.75rem;    /* 12px */
  --fs-mono:    0.8125rem;  /* 13px */

  /* Line heights */
  --lh-display: 1.1;
  --lh-heading: 1.2;
  --lh-body:    1.7;
  --lh-ui:      1.4;

  /* Letter spacing */
  --ls-display: -0.02em;
  --ls-label:    0.06em;
}
```

---

## Usage rules

- **Figtree** — every heading, button label, nav item, tag, and UI element. Never use it for running body copy.
- **Source Serif 4** — all body text in documents and long-form web copy. Italic variant for pull quotes and callouts.
- **JetBrains Mono** — IFC schema names, file extensions, code snippets, version strings. Never for decorative use.
- **No system fonts** — Arial, Calibri, and Times New Roman are forbidden in all externally distributed materials.
- **No substitutions** — if a font fails to load, fix the font. Do not substitute.
- **PowerPoint minimum** — 18pt hard floor. No exceptions.

---

## Colour pairings for type

| Text | Background | Usage |
|------|------------|-------|
| #041E42 Navy | white / #E3E3E3 | Primary headings on light |
| #354B55 Slate | white / #E3E3E3 | Sub-headings, secondary text |
| #38363D Charcoal | white / #E3E3E3 | Body text — replaces pure black |
| #ffffff White | #041E42 Navy | Headings and body on dark backgrounds |
| #48BF91 Mint | #041E42 Navy | Accent labels and active states on dark |
| #48BF91 Mint | white | Links and inline accents only — not large text blocks |
