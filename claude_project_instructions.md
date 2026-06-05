# buildingSMART Finland — Brand Development Project

## Who we are
buildingSMART Finland is the Finnish chapter of buildingSMART International (bSI), the global body responsible for openBIM standards: IFC, IDS, BCF, and the OpenCDE platform. We promote and develop building information modelling in Finland, with a focus on open standards and interoperability across the built environment sector.

## What this project is
We are developing a clean, minimal rebrand for buildingSMART Finland. The work lives in a GitHub repository containing two evolving documents: a visual moodboard (`bsf_moodboard.html`) and a brand direction brief (`bsf_brand_direction_brief.md`). These are the canonical source of truth — always read them before making decisions.

## Non-negotiable decisions (already locked)
- We use the **secondary** bSI palette only. The primary palette (red `#e5172a`, royal blue `#004f9f`, magenta `#9f3588`) is off-limits.
- The visual language is **clean and minimal** — generous whitespace, typographic hierarchy over colour decoration, no gradients.
- **Mint (`#48BF91`) is the single accent colour.** One mint element per composition. Never two.

## The secondary palette and roles
| Name | Hex | Role |
|------|-----|------|
| Deep Navy | `#041E42` | Primary anchor, headings, hero backgrounds |
| Dark Slate | `#354b55` | Secondary surfaces, supporting darks |
| Charcoal | `#38363d` | Body text, UI elements |
| Mint | `#48BF91` | Sole accent — CTAs, highlights, brand signature |
| Silver Gray | `#C8C6C5` | Borders, dividers, muted UI |
| Light Gray | `#e3e3e3` | Page backgrounds, card surfaces |

## Typography system
- **Display/headlines:** Plus Jakarta Sans — weights 600, 700, 800
- **Body/UI:** Inter — weights 400, 500, 600
- **Technical/code:** JetBrains Mono — for standards identifiers (IFC, IDS, BCF, IfcWall, etc.)
- All three are available free via Google Fonts.

## Three defined directions
**01 Nordic Blueprint** — Deep navy dominant, mint as sole accent, slate for depth. For events, print, premium touchpoints. Maximum differentiation from the bSI primary brand.

**02 Open Ground** — Light/white ground, charcoal + navy text hierarchy, mint for interactions. For web, email, documentation. Most accessible and easiest to implement.

**03 Deep Slate** — Slate as hero ground, navy for depth, mint accent. Architectural and premium. For brand hero moments, covers, awards.

**Recommended hybrid:** Open Ground as the digital default; Nordic Blueprint for event/publication presence. Both share the same palette and type system.

## Six design principles
1. One accent rule — mint appears once per composition
2. Whitespace is structure — generous margins, don't fill space
3. Type does the work — hierarchy through weight and size, not colour variation
4. Technical precision — JetBrains Mono wherever standards identifiers appear
5. Chapter, not copy — never reach for the primary bSI red or magenta
6. Geometric, not illustrative — rectangles, grids, thin rules; no organic illustration

## How to work in this project
- The user will share current file contents or ask you to work from the uploaded files.
- Before proposing any change to palette, typography, or direction, check whether it conflicts with locked decisions above.
- When proposing a change to a document, produce the full updated file (not a diff) so it can be committed to Git directly.
- If a direction change is significant (e.g. adding a new colour, changing the type pairing), state the rationale explicitly and flag it as a decision that should be committed with a descriptive commit message.
- Prefer evolving one existing direction to depth over adding new directions.
- The working language context is Finnish/English bilingual — all brand copy may be in Finnish; design principles and documentation are in English.
