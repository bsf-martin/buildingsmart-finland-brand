# buildingSMART Finland — Brand LUTs

Three `.cube` Look-Up Tables for grading photography and imagery to match the BSF brand palette. Apply them in **Affinity Photo** (v1 or v2) to make images feel at home alongside the brand colours.

## Files

| File | Direction | Character |
|------|-----------|-----------|
| `bsf_nordic_blueprint.cube` | Nordic Blueprint | Dark, cold, navy-anchored shadows |
| `bsf_open_ground.cube` | Open Ground | Clean, airy, gentle cool cast |
| `bsf_deep_slate.cube` | Deep Slate | Architectural, moody, slate midtones |

## What each LUT does

**Nordic Blueprint** — Strong cool grade. Shadows pull toward Deep Navy (`#041E42`), highlights cool toward Silver Gray. Warm tones (reds, oranges) are significantly desaturated. Best for event graphics, hero imagery, and dark-background layouts.

**Open Ground** — Gentle grade. Shadows lift softly toward Charcoal, highlights stay airy near Light Gray. Minimal desaturation of warms. Best for web, documentation, and light-background layouts.

**Deep Slate** — Architectural grade. Midtones shift toward Dark Slate (`#354b55`), shadows blend between Navy and Slate, overall slight exposure reduction. Warm tones strongly desaturated. Best for cover art, publication layouts, and premium print.

## How to apply in Affinity Photo

1. Open your image in Affinity Photo.
2. Go to **Layers → New Adjustment Layer → LUT**.
3. In the LUT panel, click **Load LUT** and browse to the `.cube` file.
4. Adjust the **Opacity** of the adjustment layer to taste — 60–80% often works better than 100% for photography with people.

## How to apply in Affinity Designer

Affinity Designer does not support LUT adjustment layers natively. The recommended workflow:

1. Place your image in Designer.
2. Open the image in **Affinity Photo** (right-click → Edit in Affinity Photo).
3. Apply the LUT there, flatten, and the graded result updates in Designer.

Alternatively, grade images before placing them: open in Photo, apply the LUT, export as a new file, then place in Designer.

## Intensity guide

| Use case | Recommended opacity |
|----------|---------------------|
| Architectural / abstract photography | 100% |
| Landscape / environmental | 80–100% |
| People / portraits | 50–70% |
| Product / object photography | 70–90% |

## Palette reference

| Name | Hex | LUT role |
|------|-----|----------|
| Deep Navy | `#041E42` | Shadow anchor (Nordic Blueprint) |
| Dark Slate | `#354B55` | Shadow/midtone anchor (Deep Slate) |
| Charcoal | `#38363D` | Shadow lift (Open Ground) |
| Silver Gray | `#C8C6C5` | Highlight target (Nordic Blueprint, Deep Slate) |
| Light Gray | `#E3E3E3` | Highlight target (Open Ground) |

Mint (`#48BF91`) is intentionally absent from the LUTs — it remains the live accent colour applied in layout, not baked into photography.
