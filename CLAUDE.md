# CLAUDE.md — buildingSMART Finland Brand & Design System

This file is read automatically by Claude Code at the start of every session. It documents project conventions, locked decisions, and working rules.

---

## What this project is

A complete design system for buildingSMART Finland — the Finnish chapter of buildingSMART International (bSI), responsible for openBIM standards (IFC, IDS, BCF, OpenCDE). The system covers visual identity, templates (PowerPoint, Word), a HTML style guide, and a Jekyll/Pandoc specification publishing pipeline.

---

## Canonical source of truth

Always read these files before making any design or code decision. When they conflict with anything else (including this file), the canonical files win.

| File | Purpose |
|------|---------|
| `bsf_brand_direction_brief.md` | Visual direction, palette roles, design principles |
| `bsf-typography.md` | Full type scale (H1–H6), CSS tokens, medium-specific rules |
| `bsf_moodboard.html` | Visual reference — established look and feel |

---

## Branch strategy

- `main` — production / stable
- `development` — active work branch; all commits go here
- Merge `development` → `main` when a phase is complete and reviewed

**Always commit to `development` unless explicitly told otherwise.**

---

## Commit conventions

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(scope): short description

- bullet detail if needed
```

Types in use:

| Type | When to use |
|------|-------------|
| `feat` | New file, section, or component added to the system |
| `fix` | Correction to existing content or code |
| `chore` | Repo structure, config, tooling, `.gitignore` |
| `docs` | Changes to markdown documentation only |
| `style` | Visual/CSS tweaks with no structural change |
| `refactor` | Restructuring without changing output |

Scope examples: `typography`, `palette`, `moodboard`, `style-guide`, `pptx`, `docs`, `structure`

Keep the subject line under 72 characters. Use bullet points in the body for anything non-trivial.

---

## Locked design decisions

These are not up for debate unless Martin explicitly says so.

### Palette — secondary bSI only

| Name | Hex | Role |
|------|-----|------|
| Deep Navy | `#041E42` | Primary anchor, headings, hero backgrounds |
| Dark Slate | `#354B55` | Secondary surfaces, supporting darks |
| Charcoal | `#38363D` | Body text, UI elements |
| Mint | `#48BF91` | **Sole accent** — one per composition, never two |
| Silver Gray | `#C8C6C5` | Borders, dividers, muted UI |
| Light Gray | `#E3E3E3` | Page backgrounds, card surfaces |

Primary bSI palette (`#E5172A`, `#004F9F`, `#9F3588`) is off-limits in all materials.

### Typography

| Role | Family | Weights |
|------|--------|---------|
| Display / H1–H6 / UI | Figtree | 600, 700, 800 |
| Body / long-form | Source Serif 4 | 400 upright; italic for callouts |
| Technical / code | JetBrains Mono | 400, 500 |

All via Google Fonts. No system fonts (Arial, Calibri, Times New Roman) in any distributed material.

**PowerPoint exception:** Figtree for all slide text. Source Serif 4 italic only in callout boxes and pull quotes — never upright on slides.

### Visual language

- Clean and minimal — generous whitespace, no gradients
- Type does the work — hierarchy through weight/size, not colour
- Geometric, not illustrative — rectangles, grids, thin rules only
- JetBrains Mono wherever standards identifiers appear (`IFC`, `IDS`, `BCF`, `IfcWall`, etc.)

---

## Repository structure

```
/
├── CLAUDE.md                        # This file
├── bsf_brand_direction_brief.md     # Canonical: visual direction
├── bsf-typography.md                # Canonical: type system
├── bsf_moodboard.html               # Visual reference
├── claude_project_instructions.md   # Cowork session instructions
├── docs/                            # Jekyll site root (GitHub Pages)
│   └── index.html                   # Phase 2: HTML style guide (complete)
├── assets/                          # Logos, images, fonts
└── luts/                            # Colour LUTs
```

`docs/` will become the full Jekyll site — eventually containing `_config.yml`, `_layouts/`, `_includes/`, and the specification publishing pipeline.

---

## Design system phases

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 1 | Foundations locked (palette, type, tokens) | ✅ Complete |
| 2 | HTML style guide (`docs/index.html`) | ✅ Complete |
| 3 | PowerPoint master template (.pptx) | ✅ Complete |
| 4 | Word document template (.dotx) | 🔄 In progress |
| 5 | HTML/CSS for Jekyll + Pandoc spec pipeline | Pending |
| 6 | PDF output (WeasyPrint via Pandoc) | Pending |
| 7 | Network member usage guide | Pending |

---

## Working rules

- Before changing any palette, type, or direction decision — check the canonical files and flag the conflict rather than silently resolving it.
- Prefer editing existing files over creating new ones unless the phase plan calls for a new deliverable.
- The project is Finnish/English bilingual — brand copy may be in Finnish; all documentation and code is in English.
- HTML files should be self-contained (single file, Google Fonts via CDN, no external dependencies beyond fonts).
- Accessibility: maintain WCAG AA contrast ratios for all text. The palette supports this — don't introduce combinations that break it.
- Never read `docs/index.html` (the style guide, about 2,000 lines) whole. Search it, or read only the lines you need.
