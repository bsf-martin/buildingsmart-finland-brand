# buildingSMART Finland — Brand Development

Visual brand direction exploration and development for buildingSMART Finland, the Finnish chapter of [buildingSMART International](https://www.buildingsmart.org). This repository tracks the evolution of the chapter's brand identity using Git for versioning and Claude (via Claude Projects) as the primary design collaborator.

---

## Context

buildingSMART Finland promotes and develops building information modelling (BIM) in Finland, with a focus on openBIM standards: IFC, IDS, BCF, and OpenCDE. The current brand is outdated and relies on the bSI primary palette (red, royal blue, magenta), which we are moving away from. This project develops a replacement identity using the **bSI secondary palette** — a cleaner, more distinctive set of colours that better serves the chapter's communications.

---

## Files

| File | Purpose |
|------|---------|
| `bsf_moodboard.html` | Visual moodboard — open in any browser. Shows the secondary palette, three brand directions, typography system, and design principles as a rendered reference. |
| `bsf_brand_direction_brief.md` | Written brand brief — the canonical text document covering colour roles, typography rationale, the three directions in detail, recommendations, and design principles. |
| `README.md` | This file. |

---

## The Secondary Palette

These are the only colours used in this brand. The bSI primary palette (red `#e5172a`, blue `#004f9f`, magenta `#9f3588`) is intentionally excluded.

| Colour | Hex | Role |
|--------|-----|------|
| Deep Navy | `#041E42` | Primary anchor, headings, hero backgrounds |
| Dark Slate | `#354b55` | Secondary surfaces, structural depth |
| Charcoal | `#38363d` | Body text, UI elements |
| **Mint** | `#48BF91` | **Sole accent — one use per composition** |
| Silver Gray | `#C8C6C5` | Borders, dividers, muted UI |
| Light Gray | `#e3e3e3` | Page backgrounds, card surfaces |

---

## Typography

| Role | Typeface | Weights |
|------|----------|---------|
| Display / Headlines | Plus Jakarta Sans | 600, 700, 800 |
| Body / UI | Inter | 400, 500, 600 |
| Technical / Code | JetBrains Mono | 400, 500 |

All three are free via Google Fonts. JetBrains Mono is reserved for standards identifiers (IFC, IDS, BCF, IfcWall, OpenCDE, etc.).

---

## Three Brand Directions

### 01 — Nordic Blueprint
Deep navy dominant, mint as the single accent, slate for secondary depth. Maximum visual differentiation from the bSI primary brand. Best for event materials, conference presence, publications, and print.

### 02 — Open Ground
Light/white ground, charcoal and navy for typographic hierarchy, mint for interactive elements. Accessible and content-first. Best for website, email, documentation, and everyday communications.

### 03 — Deep Slate
Dark slate as the hero ground, navy for depth, mint accent. Architectural and premium. Best for brand hero moments, covers, awards, and executive presentations.

**Recommended hybrid:** Open Ground as the digital default; Nordic Blueprint for event and publication presence. Both directions share the same palette and type system.

---

## Working Method

This repository pairs with a **Claude Project** for iterative brand development. The workflow:

```
Refine an idea in Claude Projects
        ↓
Claude produces updated file(s)
        ↓
Review changes (GitHub diff shows exactly what moved)
        ↓
Commit with a descriptive message
        ↓
Repeat
```

### Commit message conventions

Descriptive, decision-oriented commit messages make the log useful:

```
Add Open Ground direction as digital default recommendation
Refine mint usage rule — one accent per composition
Update typography: switch body font from Inter to DM Sans
Add social media card application mockup to moodboard
Lock Nordic Blueprint as primary event identity
```

### Working with Claude Projects

The Claude Project for this repository has instructions pre-loaded with brand context (palette, typography, directions, principles). To continue work in a session:

1. Open the Claude Project
2. Paste the current contents of the file(s) you want to evolve, or reference the uploaded versions
3. Describe what you want to explore or refine
4. Review Claude's output, request adjustments
5. When satisfied, copy the new file, commit to this repo with a clear message

---

## Design Principles

1. **One accent rule** — Mint appears once per composition. Two mint elements weakens the signature.
2. **Whitespace is structure** — Generous margins. Don't fill space.
3. **Type does the work** — Hierarchy through weight and size, not colour variation.
4. **Technical precision** — JetBrains Mono wherever standards identifiers appear.
5. **Chapter, not copy** — Never reach for the bSI primary red or magenta.
6. **Geometric, not illustrative** — Rectangles, grids, and rules; no organic illustration.

---

## Status

| Item | Status |
|------|--------|
| Secondary palette defined | ✅ Done |
| Three directions moodboarded | ✅ Done |
| Typography system defined | ✅ Done |
| Direction chosen | ⬜ Pending stakeholder feedback |
| Application mockups (web, social, print) | ⬜ Pending |
| Logo / wordmark development | ⬜ Pending |
| Final brand guidelines document | ⬜ Pending |

---

*buildingSMART Finland · Brand Development · Started June 2026*
