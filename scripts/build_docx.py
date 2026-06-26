#!/usr/bin/env python3
"""
buildingSMART Finland — Word document template generator
Run:    python3 scripts/build_docx.py
Output: templates/bsf-finland-template.dotx

Fonts required locally (Google Fonts — install before opening):
  Figtree (all weights including SemiBold and ExtraBold), Source Serif 4, JetBrains Mono
Regenerate after any design-token change.
"""

import io
import os
import zipfile

from lxml import etree
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Brand tokens ──────────────────────────────────────────────────────────────

NAVY_HEX     = '041E42'
SLATE_HEX    = '354B55'
CHARCOAL_HEX = '38363D'
MINT_HEX     = '48BF91'
SILVER_HEX   = 'C8C6C5'
LGRAY_HEX    = 'E3E3E3'
WHITE_HEX    = 'FFFFFF'

def rgb(h):
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

NAVY     = rgb(NAVY_HEX)
SLATE    = rgb(SLATE_HEX)
CHARCOAL = rgb(CHARCOAL_HEX)
SILVER   = rgb(SILVER_HEX)
WHITE    = rgb(WHITE_HEX)

PAGE_W = Mm(210)
PAGE_H = Mm(297)
MARGIN = Mm(25)

# ── Unit helpers ──────────────────────────────────────────────────────────────
# Word XML spacing is in twips (1/20 pt). EMU/635 = twips.

def pt_to_twips(pt):
    return int(pt * 20)

def emu_to_twips(emu):
    return int(emu / 635)

# ── Low-level style XML helpers ───────────────────────────────────────────────

def _ppr(style_el):
    el = style_el.find(qn('w:pPr'))
    if el is None:
        el = OxmlElement('w:pPr')
        style_el.append(el)
    return el

def _rpr(style_el):
    el = style_el.find(qn('w:rPr'))
    if el is None:
        el = OxmlElement('w:rPr')
        style_el.append(el)
    return el

def _replace_child(parent, tag, new_el):
    existing = parent.find(qn(tag))
    if existing is not None:
        parent.remove(existing)
    if new_el is not None:
        parent.append(new_el)

def style_font(style_el, font_name, size_pt, bold=False, italic=False,
               color_hex=None, all_caps=False, track_pt=None):
    """Set run-level formatting on a style element's rPr."""
    rpr = _rpr(style_el)

    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.insert(0, rfonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rfonts.set(qn(attr), font_name)

    for tag in ('w:b', 'w:bCs'):
        _replace_child(rpr, tag, OxmlElement(tag) if bold else None)
    for tag in ('w:i', 'w:iCs'):
        _replace_child(rpr, tag, OxmlElement(tag) if italic else None)

    caps_el = OxmlElement('w:caps') if all_caps else None
    _replace_child(rpr, 'w:caps', caps_el)

    if track_pt is not None:
        sp = OxmlElement('w:spacing')
        sp.set(qn('w:val'), str(pt_to_twips(track_pt)))
        _replace_child(rpr, 'w:spacing', sp)

    half = str(int(size_pt * 2))
    for tag in ('w:sz', 'w:szCs'):
        el = OxmlElement(tag)
        el.set(qn('w:val'), half)
        _replace_child(rpr, tag, el)

    if color_hex:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), color_hex)
        _replace_child(rpr, 'w:color', c)

def style_spacing(style_el, before_pt=0, after_pt=0, line_x=None):
    """Set paragraph spacing on a style element's pPr.
    line_x is a multiplier (e.g. 1.7); stored as 240ths-of-a-line."""
    ppr = _ppr(style_el)
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(pt_to_twips(before_pt)))
    sp.set(qn('w:after'), str(pt_to_twips(after_pt)))
    if line_x is not None:
        sp.set(qn('w:line'), str(int(round(line_x * 240))))
        sp.set(qn('w:lineRule'), 'auto')
    _replace_child(ppr, 'w:spacing', sp)

def style_shading(style_el, fill_hex):
    ppr = _ppr(style_el)
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    _replace_child(ppr, 'w:shd', shd)

def style_left_border(style_el, color_hex, sz_eighths=24, space=6):
    ppr = _ppr(style_el)
    pb = ppr.find(qn('w:pBdr'))
    if pb is None:
        pb = OxmlElement('w:pBdr')
        ppr.append(pb)
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), str(sz_eighths))
    left.set(qn('w:space'), str(space))
    left.set(qn('w:color'), color_hex)
    _replace_child(pb, 'w:left', left)

def style_indent(style_el, left_mm=None, right_mm=None):
    ppr = _ppr(style_el)
    ind = OxmlElement('w:ind')
    if left_mm is not None:
        ind.set(qn('w:left'), str(emu_to_twips(Mm(left_mm))))
    if right_mm is not None:
        ind.set(qn('w:right'), str(emu_to_twips(Mm(right_mm))))
    _replace_child(ppr, 'w:ind', ind)

def style_keep_next(style_el):
    ppr = _ppr(style_el)
    if ppr.find(qn('w:keepNext')) is None:
        ppr.append(OxmlElement('w:keepNext'))

# ── Run-level helpers (for content, not styles) ───────────────────────────────

def run_color(run, hex_str):
    rpr = run._r.get_or_add_rPr()
    c = OxmlElement('w:color')
    c.set(qn('w:val'), hex_str)
    _replace_child(rpr, 'w:color', c)

def styled_run(para, text, font_name, size_pt, bold=False, italic=False,
               color_hex=None):
    r = para.add_run(text)
    r.font.name   = font_name
    r.font.size   = Pt(size_pt)
    r.font.bold   = bold
    r.font.italic = italic
    if color_hex:
        run_color(r, color_hex)
    return r

def field_run(para, instr, font_name='Figtree', size_pt=8, color_hex=SILVER_HEX):
    """Insert a Word field (e.g. PAGE) into a paragraph."""
    for ftype, text in [('begin', None), (None, instr), ('end', None)]:
        r = para.add_run()
        r.font.name = font_name
        r.font.size = Pt(size_pt)
        run_color(r, color_hex)
        if ftype:
            fld = OxmlElement('w:fldChar')
            fld.set(qn('w:fldCharType'), ftype)
            r._r.append(fld)
        else:
            ins = OxmlElement('w:instrText')
            ins.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            ins.text = f' {instr} '
            r._r.append(ins)

def para_tab_stop(para, pos_emu, align='right'):
    ppr = para._p.get_or_add_pPr()
    tabs = ppr.find(qn('w:tabs'))
    if tabs is None:
        tabs = OxmlElement('w:tabs')
        ppr.append(tabs)
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), align)
    tab.set(qn('w:pos'), str(emu_to_twips(pos_emu)))
    tabs.append(tab)

def para_border(para, side, color_hex=SILVER_HEX, sz=4, space=4):
    ppr = para._p.get_or_add_pPr()
    pb = ppr.find(qn('w:pBdr'))
    if pb is None:
        pb = OxmlElement('w:pBdr')
        ppr.append(pb)
    b = OxmlElement(f'w:{side}')
    b.set(qn('w:val'), 'single')
    b.set(qn('w:sz'), str(sz))
    b.set(qn('w:space'), str(space))
    b.set(qn('w:color'), color_hex)
    _replace_child(pb, f'w:{side}', b)

def para_spacing(para, before_pt=0, after_pt=0):
    ppr = para._p.get_or_add_pPr()
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:before'), str(pt_to_twips(before_pt)))
    sp.set(qn('w:after'), str(pt_to_twips(after_pt)))
    _replace_child(ppr, 'w:spacing', sp)

def cell_shading(cell, fill_hex):
    tcp = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    _replace_child(tcp, 'w:shd', shd)

def cell_border(cell, side, color_hex, sz_eighths=12, space=0):
    """Add a border to one side of a table cell (sz_eighths: eighths of a point)."""
    tcp = cell._tc.get_or_add_tcPr()
    borders = tcp.find(qn('w:tcBorders'))
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tcp.append(borders)
    b = OxmlElement(f'w:{side}')
    b.set(qn('w:val'), 'single')
    b.set(qn('w:sz'), str(sz_eighths))
    b.set(qn('w:space'), str(space))
    b.set(qn('w:color'), color_hex)
    _replace_child(borders, f'w:{side}', b)

def cell_no_border(cell, side):
    """Suppress a border on one side of a table cell."""
    tcp = cell._tc.get_or_add_tcPr()
    borders = tcp.find(qn('w:tcBorders'))
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tcp.append(borders)
    b = OxmlElement(f'w:{side}')
    b.set(qn('w:val'), 'none')
    b.set(qn('w:sz'), '0')
    b.set(qn('w:space'), '0')
    b.set(qn('w:color'), 'auto')
    _replace_child(borders, f'w:{side}', b)

def set_col_width(table, col_idx, width_mm):
    for row in table.rows:
        tc = row.cells[col_idx]._tc
        tcp = tc.get_or_add_tcPr()
        tcw = tcp.find(qn('w:tcW'))
        if tcw is None:
            tcw = OxmlElement('w:tcW')
            tcp.append(tcw)
        tcw.set(qn('w:w'), str(emu_to_twips(Mm(width_mm))))
        tcw.set(qn('w:type'), 'dxa')

# ── Get / add style ───────────────────────────────────────────────────────────

def _get_or_add(doc, name, stype='paragraph', base=None):
    from docx.enum.style import WD_STYLE_TYPE
    tmap = {'paragraph': WD_STYLE_TYPE.PARAGRAPH, 'character': WD_STYLE_TYPE.CHARACTER}
    try:
        return doc.styles[name]
    except KeyError:
        st = doc.styles.add_style(name, tmap[stype])
        if base:
            try:
                st.base_style = doc.styles[base]
            except KeyError:
                pass
        return st

# ── Page layout ───────────────────────────────────────────────────────────────

def set_page_layout(doc):
    s = doc.sections[0]
    s.page_width      = PAGE_W
    s.page_height     = PAGE_H
    s.top_margin      = MARGIN
    s.bottom_margin   = MARGIN
    s.left_margin     = MARGIN
    s.right_margin    = MARGIN

# ── Office theme patch ────────────────────────────────────────────────────────

def patch_theme(doc):
    part = doc.part
    theme_rel = next((r for r in part.rels.values() if 'theme' in r.reltype), None)
    if not theme_rel:
        return
    tp = theme_rel.target_part
    NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    T = lambda n: f'{{{NS}}}{n}'

    tree = etree.fromstring(tp.blob)

    clr = tree.find('.//' + T('clrScheme'))
    if clr is not None:
        for slot, val in {
            'dk1': NAVY_HEX, 'lt1': WHITE_HEX,
            'dk2': CHARCOAL_HEX, 'lt2': LGRAY_HEX,
            'accent1': MINT_HEX, 'accent2': SLATE_HEX,
            'accent3': SILVER_HEX, 'accent4': NAVY_HEX,
            'accent5': SLATE_HEX, 'accent6': MINT_HEX,
        }.items():
            el = clr.find(T(slot))
            if el is not None:
                for ch in list(el):
                    el.remove(ch)
                etree.SubElement(el, T('srgbClr')).set('val', val)

    fs = tree.find('.//' + T('fontScheme'))
    if fs is not None:
        for role in ('majorFont', 'minorFont'):
            fn = fs.find(T(role))
            if fn is not None:
                lat = fn.find(T('latin'))
                if lat is None:
                    lat = etree.SubElement(fn, T('latin'))
                lat.set('typeface', 'Figtree')

    tp._blob = etree.tostring(tree, xml_declaration=True,
                              encoding='UTF-8', standalone=True)

# ── Style definitions ─────────────────────────────────────────────────────────
#
# Word type scale — from bsf-typography.md:
#   Display  36pt  800  Figtree ExtraBold  cover title only
#   H1       27pt  700  Figtree            Navy
#   H2       21pt  700  Figtree            Navy
#   H3       16pt  600  Figtree SemiBold   Navy
#   H4       14pt  600  Figtree SemiBold   Navy
#   H5       12pt  600  Figtree SemiBold   Navy
#   H6       10pt  600  Figtree SemiBold   Slate, ALL CAPS, +tracking
#   Normal   12pt  400  Source Serif 4     Charcoal
#   Caption  10.5pt 400 Source Serif 4     Charcoal
#   Label     9pt  600  Figtree SemiBold   Slate, ALL CAPS, +tracking
#   Mono     10pt  400  JetBrains Mono     Charcoal

def define_styles(doc):

    # Normal — the base for everything
    normal = doc.styles['Normal']
    style_font(normal.element, 'Source Sans 3', 12, color_hex=CHARCOAL_HEX)
    style_spacing(normal.element, before_pt=0, after_pt=8, line_x=1.7)

    # Headings — H1/H2 bold 700; H3–H5 SemiBold 600; H6 SemiBold 600 Slate caps
    # (name, font_name, size, bold, color, before, after, kwn, caps, track_pt)
    hdefs = [
        ('Heading 1', 'Figtree',           27,  True,  NAVY_HEX,  24, 6,  True,  False, None),
        ('Heading 2', 'Figtree',           21,  True,  NAVY_HEX,  18, 4,  True,  False, None),
        ('Heading 3', 'Figtree SemiBold',  16,  False, NAVY_HEX,  14, 4,  True,  False, None),
        ('Heading 4', 'Figtree SemiBold',  14,  False, NAVY_HEX,  10, 3,  False, False, None),
        ('Heading 5', 'Figtree SemiBold',  12,  False, NAVY_HEX,   8, 3,  False, False, None),
        ('Heading 6', 'Figtree SemiBold',  10,  False, SLATE_HEX,  6, 3,  False, True,  0.6),
    ]
    for name, fn, sz, bold, col, bef, aft, kwn, caps, trk in hdefs:
        st = doc.styles[name]
        style_font(st.element, fn, sz, bold=bold, color_hex=col,
                   all_caps=caps, track_pt=trk)
        style_spacing(st.element, before_pt=bef, after_pt=aft, line_x=1.2)
        if kwn:
            style_keep_next(st.element)

    # BSF Display — cover page title (36pt ExtraBold Navy)
    disp = _get_or_add(doc, 'BSF Display', base='Normal')
    style_font(disp.element, 'Figtree ExtraBold', 36, color_hex=NAVY_HEX)
    style_spacing(disp.element, before_pt=0, after_pt=6, line_x=1.1)

    # Block Quotation — Source Serif 4 italic, Mint left border baked into style
    bq = _get_or_add(doc, 'Block Quotation', base='Normal')
    style_font(bq.element, 'Source Serif 4', 12, italic=True, color_hex=SLATE_HEX)
    style_spacing(bq.element, before_pt=12, after_pt=12, line_x=1.7)
    style_left_border(bq.element, MINT_HEX, sz_eighths=24, space=6)
    style_indent(bq.element, left_mm=8)

    # Code — JetBrains Mono, Light Gray shading baked into style
    code = _get_or_add(doc, 'Code', base='Normal')
    style_font(code.element, 'JetBrains Mono', 10, color_hex=CHARCOAL_HEX)
    style_spacing(code.element, before_pt=6, after_pt=6, line_x=1.4)
    style_shading(code.element, LGRAY_HEX)
    style_indent(code.element, left_mm=5, right_mm=5)

    # Caption — Source Sans 3 10.5pt
    cap = _get_or_add(doc, 'Caption', base='Normal')
    style_font(cap.element, 'Source Sans 3', 10.5, color_hex=CHARCOAL_HEX)
    style_spacing(cap.element, before_pt=3, after_pt=8, line_x=1.4)

    # BSF Label — small Figtree SemiBold all-caps with tracking
    lbl = _get_or_add(doc, 'BSF Label', base='Normal')
    style_font(lbl.element, 'Figtree SemiBold', 9, color_hex=SLATE_HEX,
               all_caps=True, track_pt=0.54)   # 0.06em × 9pt
    style_spacing(lbl.element, before_pt=3, after_pt=3, line_x=1.4)

    # BSF Block Attribution — label style with Mint left border, matching Block Quotation.
    # Use this for the cite/attribution line that follows a Block Quotation paragraph so
    # the Mint border runs continuously through both quote and attribution.
    ba = _get_or_add(doc, 'BSF Block Attribution', base='Normal')
    style_font(ba.element, 'Figtree SemiBold', 9, color_hex=SLATE_HEX,
               all_caps=True, track_pt=0.54)
    style_spacing(ba.element, before_pt=0, after_pt=12, line_x=1.4)
    style_left_border(ba.element, MINT_HEX, sz_eighths=24, space=6)
    style_indent(ba.element, left_mm=8)

    # Inline Code — character style for inline IFC/IDS/BCF identifiers
    ic = _get_or_add(doc, 'Inline Code', stype='character')
    rpr = ic.element.find(qn('w:rPr'))
    if rpr is None:
        rpr = OxmlElement('w:rPr')
        ic.element.append(rpr)
    rfonts = OxmlElement('w:rFonts')
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rfonts.set(qn(attr), 'JetBrains Mono')
    _replace_child(rpr, 'w:rFonts', rfonts)
    for tag in ('w:sz', 'w:szCs'):
        el = OxmlElement(tag)
        el.set(qn('w:val'), '20')   # 10pt = 20 half-points
        _replace_child(rpr, tag, el)

    # BSF Table Header — Figtree SemiBold Navy, no fill, bottom border applied per-cell
    # Matches property-set table style in style guide: label-style, tracked, no background
    th = _get_or_add(doc, 'BSF Table Header', base='Normal')
    style_font(th.element, 'Figtree SemiBold', 10, color_hex=NAVY_HEX, track_pt=0.1)
    style_spacing(th.element, before_pt=0, after_pt=12, line_x=1.4)

    # BSF Table Body — Source Sans 3 for description cells
    tn = _get_or_add(doc, 'BSF Table Normal', base='Normal')
    style_font(tn.element, 'Source Sans 3', 10.5, color_hex=CHARCOAL_HEX)
    style_spacing(tn.element, before_pt=2, after_pt=2, line_x=1.4)

# ── Header / Footer ───────────────────────────────────────────────────────────

CONTENT_W = PAGE_W - MARGIN * 2   # 160mm in EMU

def setup_header(section):
    hdr = section.header
    hdr.is_linked_to_previous = False
    para = hdr.paragraphs[0]
    para.clear()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para_border(para, 'bottom')
    para_tab_stop(para, CONTENT_W, align='right')

    styled_run(para, 'buildingSMART Finland', 'JetBrains Mono', 8,
               color_hex=SILVER_HEX)
    para.add_run('\t').font.size = Pt(8)
    styled_run(para, 'Chapter Title', 'Figtree SemiBold', 8,
               color_hex=SILVER_HEX)

def setup_footer(section):
    ftr = section.footer
    ftr.is_linked_to_previous = False
    para = ftr.paragraphs[0]
    para.clear()
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    para_border(para, 'top')
    para_tab_stop(para, CONTENT_W, align='right')

    styled_run(para, 'buildingSMART Finland', 'JetBrains Mono', 8,
               color_hex=SILVER_HEX)
    para.add_run('\t').font.size = Pt(8)
    field_run(para, 'PAGE', font_name='Figtree', size_pt=8, color_hex=SILVER_HEX)

# ── Cover page ────────────────────────────────────────────────────────────────

def add_cover_page(doc):
    # Display title — 36pt Figtree ExtraBold Navy
    p = doc.add_paragraph(style='BSF Display')
    styled_run(p, 'Document Title', 'Figtree ExtraBold', 36,
               color_hex=NAVY_HEX)

    # Mint rule
    rule = doc.add_paragraph()
    para_spacing(rule, before_pt=0, after_pt=0)
    para_border(rule, 'bottom', color_hex=MINT_HEX, sz=6, space=4)

    # Subtitle — Source Serif 4 italic
    sub = doc.add_paragraph()
    para_spacing(sub, before_pt=10, after_pt=4)
    styled_run(sub, 'Subtitle or document description', 'Source Serif 4', 14,
               italic=True, color_hex=SLATE_HEX)

    # Meta — JetBrains Mono
    meta = doc.add_paragraph()
    para_spacing(meta, before_pt=6, after_pt=48)
    styled_run(meta, 'MONTH YEAR  ·  buildingSMART Finland',
               'JetBrains Mono', 9, color_hex=CHARCOAL_HEX)

    doc.add_page_break()

# ── Sample body content ───────────────────────────────────────────────────────

def add_sample_content(doc):
    doc.add_heading('1  Section Heading', level=1)

    doc.add_paragraph(
        'Body text in Source Serif 4 at 12pt, Charcoal, 1.7× line height. '
        'This is the Normal paragraph style. Use it for all running body text in '
        'reports, specifications, and guidance notes.'
    )

    doc.add_heading('1.1  Sub-section Heading', level=2)

    doc.add_paragraph(
        'A second body paragraph. Headings carry keep-with-next so they never '
        'orphan at a page break. Note 8pt space after each Normal paragraph.'
    )

    doc.add_paragraph(
        '“Block Quotation: Source Serif 4 italic 12pt Slate, with a 3pt Mint '
        'left border baked into the style. Apply the Block Quotation style — '
        'do not add the border manually.”',
        style='Block Quotation'
    )
    doc.add_paragraph('— BUILDINGSMART INTERNATIONAL', style='BSF Block Attribution')

    doc.add_heading('1.1.1  Clause Heading', level=3)

    doc.add_paragraph(
        'IfcWall IFCWALL_001 {\n'
        '  Name           = "External Wall";\n'
        '  PredefinedType = .STANDARD.;\n'
        '}',
        style='Code'
    )
    doc.add_paragraph(
        'Figure 1 — IFC entity example. Caption: Source Serif 4 10.5pt.',
        style='Caption'
    )

    doc.add_heading('1.1.1.1  Standards Identifiers', level=4)

    p = doc.add_paragraph('Standards identifiers such as ')
    r = p.add_run('IFC, IDS, BCF, IfcWall')
    r.font.name = 'JetBrains Mono'
    r.font.size = Pt(10)
    run_color(r, CHARCOAL_HEX)
    p.add_run(' appear inline in JetBrains Mono via the Inline Code character style.')

    doc.add_heading('Heading 5 — Figtree SemiBold 12pt Navy', level=5)
    doc.add_heading('HEADING 6 — FIGTREE SEMIBOLD 10PT SLATE TRACKED CAPS', level=6)

    doc.add_paragraph('DOCUMENT TYPE', style='BSF Label')
    doc.add_paragraph(
        'BSF Label: Figtree SemiBold 9pt Slate, all caps, 0.06em tracking.'
    )

def add_sample_table(doc):
    """Property set table — matches the IFC Pset example in the HTML style guide.

    Header: Figtree SemiBold 10pt Navy, no fill, 2pt Navy bottom border.
    Col 1 (property name): JetBrains Mono 10pt Charcoal.
    Col 2 (type):          JetBrains Mono 10pt Slate.
    Col 3 (description):   Source Serif 4 10.5pt Charcoal.
    Alternating rows: subtle Light Gray on odd data rows.
    """
    doc.add_heading('1.2  Property Set Table', level=2)
    doc.add_paragraph(
        'Specification-style table. Column headers in Figtree SemiBold Navy; '
        'property names and types in JetBrains Mono; descriptions in Source Serif 4.',
        style='Caption'
    )

    headers = ['Property name', 'Type', 'Description']
    rows_data = [
        ('IsExternal',           'IfcBoolean',                      'Indicates whether the element is positioned at the external face of the building envelope.'),
        ('LoadBearing',          'IfcBoolean',                      'Indicates whether the element is load-bearing. This is a design intent — structural analysis governs.'),
        ('FireRating',           'IfcLabel',                        'Fire rating classification according to the relevant national standard. Free-text label — validate against project requirements.'),
        ('ThermalTransmittance', 'IfcThermalTransmittanceMeasure',  'Overall thermal transmittance (U-value) of the element, in W/m²K. Required for energy performance calculations.'),
    ]

    # Col widths: name 40mm, type 48mm, description 72mm (total 160mm = content width)
    COL_W = [40, 48, 72]

    tbl = doc.add_table(rows=1 + len(rows_data), cols=3)
    tbl.style = 'Normal Table'   # no borders from style; we add what we need manually

    # Set column widths
    for ci, w in enumerate(COL_W):
        set_col_width(tbl, ci, w)

    # ── Header row ──
    hdr_row = tbl.rows[0]
    for ci, label in enumerate(headers):
        cell = hdr_row.cells[ci]
        p = cell.paragraphs[0]
        p.clear()
        styled_run(p, label, 'Figtree SemiBold', 10, color_hex=NAVY_HEX)
        # Bottom border: 2pt (16 eighths) solid Navy; suppress all other borders
        cell_border(cell, 'bottom', NAVY_HEX, sz_eighths=16)
        for side in ('top', 'left', 'right', 'insideH', 'insideV'):
            cell_no_border(cell, side)

    # ── Data rows ──
    for ri, (prop, typ, desc) in enumerate(rows_data):
        row = tbl.rows[ri + 1]
        shade = ri % 2 == 0   # odd rows (0-indexed): Light Gray

        # Col 0 — property name: JetBrains Mono Charcoal
        c0 = row.cells[0]
        c0.paragraphs[0].clear()
        styled_run(c0.paragraphs[0], prop, 'JetBrains Mono', 10, color_hex=CHARCOAL_HEX)

        # Col 1 — type: JetBrains Mono Slate
        c1 = row.cells[1]
        c1.paragraphs[0].clear()
        styled_run(c1.paragraphs[0], typ, 'JetBrains Mono', 10, color_hex=SLATE_HEX)

        # Col 2 — description: Source Serif 4 Charcoal
        c2 = row.cells[2]
        c2.paragraphs[0].clear()
        styled_run(c2.paragraphs[0], desc, 'Source Sans 3', 10.5, color_hex=CHARCOAL_HEX)

        if shade:
            for cell in [c0, c1, c2]:
                cell_shading(cell, LGRAY_HEX)

        # Suppress all borders on data cells
        for cell in [c0, c1, c2]:
            for side in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV'):
                cell_no_border(cell, side)

# ── .dotx conversion ──────────────────────────────────────────────────────────

def convert_to_dotx(docx_path, dotx_path):
    DOCX_CT = b'wordprocessingml.document.main+xml'
    DOTX_CT = b'wordprocessingml.template.main+xml'
    buf = io.BytesIO()
    with zipfile.ZipFile(docx_path, 'r') as zin:
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == '[Content_Types].xml':
                    data = data.replace(DOCX_CT, DOTX_CT)
                zout.writestr(item, data)
    with open(dotx_path, 'wb') as f:
        f.write(buf.getvalue())

# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    doc = Document()
    set_page_layout(doc)
    patch_theme(doc)
    define_styles(doc)
    setup_header(doc.sections[0])
    setup_footer(doc.sections[0])
    add_cover_page(doc)
    add_sample_content(doc)
    add_sample_table(doc)

    here     = os.path.dirname(os.path.abspath(__file__))
    out_dir  = os.path.realpath(os.path.join(here, '..', 'templates'))
    os.makedirs(out_dir, exist_ok=True)
    tmp      = os.path.join(out_dir, '_bsf_tmp.docx')
    dotx     = os.path.join(out_dir, 'bsf-finland-template.dotx')

    doc.save(tmp)
    convert_to_dotx(tmp, dotx)
    os.remove(tmp)
    print(f'Saved → {dotx}')


if __name__ == '__main__':
    build()
