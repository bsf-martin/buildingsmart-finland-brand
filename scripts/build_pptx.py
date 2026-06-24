#!/usr/bin/env python3
"""
buildingSMART Finland — PowerPoint master template generator
Run:    python3 scripts/build_pptx.py
Output: templates/bsf-finland-template.pptx

Regenerate this file after any design-token change.
Logo: SVG source is at assets/images/logos/buildingsmart_finland_logo_white.svg.
      A text wordmark is used until a PNG/EMF export is available.
"""

import os
from lxml import etree

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

# ── Brand tokens ──────────────────────────────────────────────────────────────

NAVY      = RGBColor(0x04, 0x1E, 0x42)
SLATE     = RGBColor(0x35, 0x4B, 0x55)
CHARCOAL  = RGBColor(0x38, 0x36, 0x3D)
MINT      = RGBColor(0x48, 0xBF, 0x91)
SILVER    = RGBColor(0xC8, 0xC6, 0xC5)
LGRAY     = RGBColor(0xE3, 0xE3, 0xE3)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
MINT_MUTE = RGBColor(0xB0, 0xD8, 0xC6)   # muted mint tint for subtitles on dark

# Slide dimensions — 16:9 widescreen
W = Inches(13.333)
H = Inches(7.5)

# Layout grid
ML = Inches(0.9)    # margin left
MR = Inches(0.9)    # margin right
MT = Inches(0.65)   # margin top
CW = W - ML - MR    # content width

# ── Shape helpers ─────────────────────────────────────────────────────────────

def rect(slide, left, top, width, height, fill, no_line=True):
    shp = slide.shapes.add_shape(1, left, top, width, height)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if no_line:
        shp.line.fill.background()
    return shp


def textbox(slide, left, top, width, height, text,
            font="Figtree", size=20, bold=False, italic=False,
            color=WHITE, align=PP_ALIGN.LEFT, wrap=True, spacing_after=0):
    txb = slide.shapes.add_textbox(left, top, width, height)
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing_after:
        p.space_after = Pt(spacing_after)
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return txb


def solid_bg(slide, color):
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = color


def mint_rule_v(slide, width_pt=5, height=None):
    """Vertical Mint rule — left edge of slide."""
    rect(slide, 0, 0, Pt(width_pt), height or H, MINT)


def mint_rule_h(slide, top, left=None, width=None, thick_pt=2):
    """Horizontal Mint rule."""
    rect(slide, left or ML, top, width or CW, Pt(thick_pt), MINT)


def wordmark_light(slide):
    """White wordmark for dark-background slides (top-left)."""
    textbox(slide, ML, Inches(0.38), Inches(5), Inches(0.38),
            "buildingSMART Finland",
            font="Figtree", size=11, bold=True, color=WHITE)


def wordmark_dark(slide):
    """Slate wordmark for light-background slides (bottom-right)."""
    textbox(slide,
            W - Inches(3.2), H - Inches(0.42),
            Inches(3.0), Inches(0.32),
            "buildingSMART Finland",
            font="Figtree", size=9, color=SLATE,
            align=PP_ALIGN.RIGHT)


# ── Theme XML patch ───────────────────────────────────────────────────────────

def set_theme_colors(prs):
    """Wire brand colours into the Office accent palette via direct XML edit."""
    sm_part = prs.slide_master.part
    theme_rel = next(r for r in sm_part.rels.values() if 'theme' in r.reltype)
    theme_part = theme_rel.target_part

    NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    tree = etree.fromstring(theme_part.blob)

    def tag(local):
        return '{%s}%s' % (NS, local)

    clr = tree.find('.//' + tag('clrScheme'))
    if clr is None:
        return

    slots = {
        'dk1':     '041E42',   # Deep Navy   — dark text / headings
        'lt1':     'FFFFFF',   # White
        'dk2':     '38363D',   # Charcoal    — body text
        'lt2':     'E3E3E3',   # Light Gray  — backgrounds
        'accent1': '48BF91',   # Mint        — sole accent
        'accent2': '354B55',   # Dark Slate  — secondary surface
        'accent3': 'C8C6C5',   # Silver Gray — borders / dividers
        'accent4': '041E42',
        'accent5': '354B55',
        'accent6': '48BF91',
    }
    for local, val in slots.items():
        el = clr.find(tag(local))
        if el is not None:
            for child in list(el):
                el.remove(child)
            srgb = etree.SubElement(el, tag('srgbClr'))
            srgb.set('val', val)

    # Font scheme — Figtree as both major and minor face
    fs = tree.find('.//' + tag('fontScheme'))
    if fs is not None:
        for role in ('majorFont', 'minorFont'):
            fn = fs.find(tag(role))
            if fn is not None:
                lat = fn.find(tag('latin'))
                if lat is not None:
                    lat.set('typeface', 'Figtree')
                else:
                    lat = etree.SubElement(fn, tag('latin'))
                    lat.set('typeface', 'Figtree')

    theme_part._blob = etree.tostring(tree, xml_declaration=True,
                                      encoding='UTF-8', standalone=True)


# ── Slide 1 — Cover ───────────────────────────────────────────────────────────

def slide_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    solid_bg(slide, NAVY)
    mint_rule_v(slide, width_pt=5)
    wordmark_light(slide)

    # Short Mint rule above title — geometric accent
    rect(slide, ML, Inches(1.75), Inches(1.4), Pt(2), MINT)

    # Display title
    textbox(slide, ML, Inches(1.95), Inches(10.2), Inches(2.0),
            "Presentation Title",
            size=40, bold=True, color=WHITE)

    # Subtitle
    textbox(slide, ML, Inches(4.0), Inches(9.5), Inches(0.65),
            "Subtitle or event name",
            size=22, color=MINT_MUTE)

    # Version / date — JetBrains Mono
    textbox(slide, ML, Inches(4.75), Inches(7.0), Inches(0.4),
            "MONTH YEAR  ·  buildingSMART Finland",
            font="JetBrains Mono", size=11, color=MINT)

    # Geo decoration — thin vertical rule on right third
    rect(slide, W - Inches(4.0), 0, Pt(1), H, RGBColor(0x48, 0xBF, 0x91))


# ── Slide 2 — Section Header ──────────────────────────────────────────────────

def slide_section_header(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    solid_bg(slide, SLATE)
    mint_rule_v(slide, width_pt=5)
    wordmark_light(slide)

    # Section number
    textbox(slide, ML, Inches(2.5), Inches(2.0), Inches(0.4),
            "01",
            font="JetBrains Mono", size=13, color=MINT)

    # Section title
    textbox(slide, ML, Inches(2.95), Inches(10.5), Inches(1.4),
            "Section Title",
            size=36, bold=True, color=WHITE)

    # Mint rule below title
    mint_rule_h(slide, top=Inches(4.5), width=Inches(3.6))


# ── Slide 3 — Title + Content ─────────────────────────────────────────────────

def slide_title_content(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    solid_bg(slide, WHITE)

    # Heading
    textbox(slide, ML, MT, CW, Inches(0.75),
            "Slide Heading",
            size=28, bold=True, color=NAVY)

    # Rule under heading
    mint_rule_h(slide, top=Inches(1.5), thick_pt=1.5)

    # Mint left accent line alongside body
    rect(slide, Inches(0.6), Inches(1.65), Pt(3.5), Inches(4.4), MINT)

    # Body text
    txb = slide.shapes.add_textbox(ML, Inches(1.7), CW, Inches(4.3))
    tf = txb.text_frame
    tf.word_wrap = True

    bullets = [
        "Body text at 20pt — Figtree 400. Minimum 18pt in all circumstances.",
        "Second bullet point. Keep slide content minimal and focused.",
        "Third bullet point. One idea per slide wherever possible.",
    ]
    for i, text in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = text
        r.font.name = "Figtree"
        r.font.size = Pt(20)
        r.font.color.rgb = CHARCOAL

    # Caption / footnote
    textbox(slide, ML, H - Inches(0.5), CW, Inches(0.38),
            "Caption or source attribution — Figtree 14pt Slate",
            size=14, color=SLATE)

    wordmark_dark(slide)


# ── Slide 4 — Two Column ──────────────────────────────────────────────────────

def slide_two_column(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    solid_bg(slide, WHITE)

    textbox(slide, ML, MT, CW, Inches(0.75),
            "Slide Heading",
            size=28, bold=True, color=NAVY)
    mint_rule_h(slide, top=Inches(1.5), thick_pt=1.5)

    col_w   = Inches(5.5)
    col_top = Inches(1.7)
    col_h   = Inches(4.5)
    gap     = Inches(0.5)
    right_l = ML + col_w + gap

    # Left column Mint rule
    rect(slide, Inches(0.6), col_top, Pt(3.5), col_h, MINT)

    # Left column text
    lx = slide.shapes.add_textbox(ML, col_top, col_w, col_h)
    lf = lx.text_frame
    lf.word_wrap = True
    for i, line in enumerate(["Left column — Figtree 20pt.",
                               "Second point in left column."]):
        p = lf.paragraphs[0] if i == 0 else lf.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = line
        r.font.name = "Figtree"
        r.font.size = Pt(20)
        r.font.color.rgb = CHARCOAL

    # Right column Mint rule
    rect(slide, right_l - Pt(8), col_top, Pt(3.5), col_h, MINT)

    # Right column text
    rx = slide.shapes.add_textbox(right_l, col_top, col_w, col_h)
    rf = rx.text_frame
    rf.word_wrap = True
    for i, line in enumerate(["Right column — Figtree 20pt.",
                               "Second point in right column."]):
        p = rf.paragraphs[0] if i == 0 else rf.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run()
        r.text = line
        r.font.name = "Figtree"
        r.font.size = Pt(20)
        r.font.color.rgb = CHARCOAL

    wordmark_dark(slide)


# ── Slide 5 — Quote / Callout ─────────────────────────────────────────────────

def slide_quote(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    solid_bg(slide, WHITE)

    # Mint left border for the quote
    rect(slide, Inches(1.6), Inches(1.9), Pt(4.5), Inches(3.6), MINT)

    # Pull quote — Source Serif 4 italic
    txb = slide.shapes.add_textbox(Inches(2.15), Inches(1.95), Inches(9.5), Inches(3.0))
    tf = txb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.space_after = Pt(16)
    r = p.add_run()
    r.text = ("“Pull quote text in Source Serif 4 italic. "
              "Two to three lines for legibility at presentation distance.”")
    r.font.name = "Source Serif 4"
    r.font.size = Pt(22)
    r.font.italic = True
    r.font.color.rgb = CHARCOAL

    # Citation — Figtree uppercase label
    textbox(slide, Inches(2.15), Inches(5.15), Inches(8.5), Inches(0.45),
            "ATTRIBUTION — TITLE OR ORGANISATION",
            font="Figtree", size=12, color=SLATE)

    wordmark_dark(slide)


# ── Slide 6 — Blank ───────────────────────────────────────────────────────────

def slide_blank(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    solid_bg(slide, WHITE)
    wordmark_dark(slide)


# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H

    set_theme_colors(prs)

    slide_cover(prs)
    slide_section_header(prs)
    slide_title_content(prs)
    slide_two_column(prs)
    slide_quote(prs)
    slide_blank(prs)

    here     = os.path.dirname(os.path.abspath(__file__))
    out_dir  = os.path.join(here, '..', 'templates')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.realpath(os.path.join(out_dir, 'bsf-finland-template.pptx'))
    prs.save(out_path)
    print(f"Saved → {out_path}")


if __name__ == '__main__':
    build()
