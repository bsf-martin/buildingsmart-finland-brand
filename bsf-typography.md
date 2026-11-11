# buildingSMART Finland — Typography Specification

## Typefaces

| Role | Family | Source |
|------|--------|--------|
| Display / Headings / UI | Figtree | Google Fonts |
| Body / Long-form | Source Sans 3 | Google Fonts |
| Quote / Emphasis | Source Serif 4 | Google Fonts · *italic only* |
| Technical / Code | JetBrains Mono | Google Fonts |

**Google Fonts import (web):**
```css
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700;800&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;1,400&family=Source+Serif+4:ital,opsz,wght@1,8..60,400;1,8..60,600&family=JetBrains+Mono:wght@400;500&display=swap');
```

---

## Type scale

### Web and document scale

| Token | Size | Weight | Family | Usage |
|-------|------|--------|--------|-------|
| display | 48px / 3rem | 800 | Figtree | Hero headlines — one per page, cover pages only |
| h1 | 36px / 2.25rem | 700 | Figtree | Document/page title — one per document |
| h2 | 28px / 1.75rem | 700 | Figtree | Major section heading |
| h3 | 22px / 1.375rem | 600 | Figtree | Sub-section heading |
| h4 | 18px / 1.125rem | 600 | Figtree | Clause-level heading |
| h5 | 16px / 1rem | 600 | Figtree | Minor heading — same size as body, weight differentiates |
| h6 | 13px / 0.8125rem | 600 | Figtree | Lowest level — uppercase, letter-spacing 0.06em |
| body | 16px / 1rem | 400 | Source Sans 3 | Running body text, paragraphs |
| quote | 16px / 1rem | 400 *italic* | Source Serif 4 | Pull quotes and callout emphasis — italic only |
| small | 14px / 0.875rem | 400 | Source Sans 3 | Captions, metadata, footnotes |
| label | 12px / 0.75rem | 600 | Figtree | UI labels — uppercase, tracking 0.06em |
| mono | 13px / 0.8125rem | 400 | JetBrains Mono | Code, schema names, file types, version strings |

### PowerPoint scale

PowerPoint uses points (pt). Body text is never smaller than **18pt**.

| Level | Size | Weight | Family | Usage |
|-------|------|--------|--------|-------|
| Title (slide title) | 36pt | 700 | Figtree | Slide title — one per slide |
| Heading 1 | 28pt | 700 | Figtree | Section title slides |
| Heading 2 | 24pt | 600 | Figtree | Content heading within a slide |
| Body | 20pt | 400 | Figtree | Primary body text on slides |
| Body small | 18pt | 400 | Figtree | Secondary body text — hard minimum |
| Callout / pull quote | 20pt | 400 *italic* | Source Serif 4 | Emphasis callout boxes and pull quotes only |
| Caption | 14pt | 400 | Figtree | Image captions, footnotes, source attribution |
| Mono | 16pt | 400 | JetBrains Mono | Standards identifiers, schema names, code |

**PowerPoint font rules:**
- Use Figtree for all slide text, including body text. Source Serif 4 appears in *italic only*, and only in callout boxes and pull quotes. Don't use it for body text.
- The template embeds the fonts, but anyone editing the slides also needs them installed (see the font installation guide in the design system).
- Don't use upright Source Serif 4 on slides. At slide sizes, an upright serif next to Figtree looks busy and clashes with the rest of the layout.

---

### Word document scale

Word uses points (pt). Minimum body size is **12pt**. The sizes come from the web scale at 1pt ≈ 1.333px, rounded to the nearest half point.

| Level | Size | Weight | Family | Usage |
|-------|------|--------|--------|-------|
| Display | 36pt | 800 | Figtree | Cover page title — one per document, cover only |
| Heading 1 | 27pt | 700 | Figtree | Document title — one per document |
| Heading 2 | 21pt | 700 | Figtree | Major section heading |
| Heading 3 | 16pt | 600 | Figtree | Sub-section heading |
| Heading 4 | 14pt | 600 | Figtree | Clause-level heading |
| Heading 5 | 12pt | 600 | Figtree | Minor heading |
| Heading 6 | 10pt | 600 | Figtree | Uppercase label — letter-spacing 0.06em |
| Body (Normal) | 12pt | 400 | Source Sans 3 | Running body text — use Named paragraph style |
| Caption | 10.5pt | 400 | Source Sans 3 | Captions, footnotes, metadata |
| Label | 9pt | 600 | Figtree | UI labels — uppercase, use sparingly |
| Mono | 10pt | 400 | JetBrains Mono | Standards identifiers, schema names, code |

**Word font rules:**
- Use the named paragraph styles for every heading level. Don't change size or weight by hand.
- Figtree for all headings (Heading 1–6). Source Sans 3 for Normal (body) and Caption.
- Source Serif 4 italic only for Block Quotation and callout emphasis, through its own paragraph style. Never upright.
- The `.dotx` template doesn't embed fonts, so they must be installed on the computer you write on.
- JetBrains Mono through its own character style, for technical names in running text.

---

## CSS tokens

```css
:root {
  /* Families */
  --ff-display: 'Figtree', sans-serif;
  --ff-body:    'Source Sans 3', system-ui, sans-serif;
  --ff-quote:   'Source Serif 4', Georgia, serif;    /* italic only — pull quotes and callout emphasis */
  --ff-mono:    'JetBrains Mono', 'Courier New', monospace;

  /* Scale — web */
  --fs-display: 3rem;        /* 48px */
  --fs-h1:      2.25rem;     /* 36px */
  --fs-h2:      1.75rem;     /* 28px */
  --fs-h3:      1.375rem;    /* 22px */
  --fs-h4:      1.125rem;    /* 18px */
  --fs-h5:      1rem;        /* 16px */
  --fs-h6:      0.8125rem;   /* 13px */
  --fs-body:    1rem;        /* 16px */
  --fs-small:   0.875rem;    /* 14px */
  --fs-label:   0.75rem;     /* 12px */
  --fs-mono:    0.8125rem;   /* 13px */

  /* Line heights */
  --lh-display: 1.1;
  --lh-heading: 1.2;
  --lh-body:    1.7;
  --lh-ui:      1.4;

  /* Letter spacing */
  --ls-display: -0.02em;
  --ls-heading: -0.01em;
  --ls-label:    0.06em;   /* Used for label and h6 */
}
```

### CSS heading styles

```css
h1, h2, h3, h4, h5, h6 {
  font-family: var(--ff-display);
  line-height: var(--lh-heading);
  letter-spacing: var(--ls-heading);
  color: #041E42;
  margin-top: 2em;
  margin-bottom: 0.5em;
}

h1 { font-size: var(--fs-h1); font-weight: 700; }
h2 { font-size: var(--fs-h2); font-weight: 700; }
h3 { font-size: var(--fs-h3); font-weight: 600; }
h4 { font-size: var(--fs-h4); font-weight: 600; }
h5 { font-size: var(--fs-h5); font-weight: 600; }
h6 {
  font-size: var(--fs-h6);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--ls-label);
  color: #354B55; /* Slate — visually recedes from H5 */
}
```

---

## Medium-specific usage rules

### All media
- **JetBrains Mono** for IFC schema names, file extensions, code and version strings (e.g. `IFC4.3`, `IfcWall`, `BCF 3.0`, `IDS`). Don't use it just for looks.
- **No system fonts.** Don't use Arial, Calibri or Times New Roman in anything we send outside the chapter.

### Web and HTML documents (Jekyll / Pandoc output)
- **Figtree** for headings H1–H6, interface elements, labels and navigation.
- **Source Sans 3** for running body text and long paragraphs.
- **Source Serif 4 italic** for pull quotes and callouts only. Never upright.
- Load the fonts from the Google Fonts CDN. Pandoc PDF output uses the same CSS through WeasyPrint.

### Word documents (.docx)
- **Figtree** for headings H1–H6, through the named paragraph styles rather than manual formatting.
- **Source Sans 3** for body text (Normal style), captions and footnotes.
- **Source Serif 4 italic** in the Block Quotation style, for pull quotes and callout emphasis only. Never upright.
- The template doesn't embed fonts, so they must be installed on the computer you write on.

### PowerPoint presentations (.pptx)
- **Figtree** for all slide text, including body text. Nothing smaller than 18pt.
- **Source Serif 4 italic** only in callout boxes and pull quotes. Never upright on slides.
- The template embeds the fonts, but you need them installed to edit. See the installation guide.
- **No substitutes.** If text shows up in Calibri, the font isn't installed. Install it before you carry on.

---

## Colour pairings for type

| Text | Background | Usage |
|------|------------|-------|
| `#041E42` Deep Navy | white / `#E3E3E3` Light Gray | Primary headings on light backgrounds |
| `#354B55` Dark Slate | white / `#E3E3E3` Light Gray | H4–H6, secondary headings, supporting text |
| `#38363D` Charcoal | white / `#E3E3E3` Light Gray | Body text — replaces pure black |
| `#FFFFFF` White | `#041E42` Deep Navy | All text on dark/navy backgrounds |
| `#FFFFFF` White | `#354B55` Dark Slate | All text on slate backgrounds |
| `#48BF91` Mint | `#041E42` Deep Navy | Accent labels and active states on dark only |
| `#48BF91` Mint | white | Not for text (2.3:1 fails WCAG). Icons, borders and indicators only |

---

*buildingSMART Finland · Typography Specification · June 2026*
