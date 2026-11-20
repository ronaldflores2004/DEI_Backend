import re, subprocess, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
src, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding='utf-8').read()
s = re.sub(r'\[([^\]]+)\]\((?!https?:)[^)]*\.md[^)]*\)', r'\1', s)       # enlaces entre documentos
s = re.sub(r'\[`?diagramas/`?\]\(diagramas/\)', '`diagramas/`', s)
s = re.sub(r'^# .*\n', '', s, count=1)
md = out + '.md'
open(md, 'w', encoding='utf-8').write(s)
subprocess.run(['pandoc', md, '-f', 'gfm', '-o', out, 
                '--resource-path=.', '-M', f'title={title}', '-M', 'subtitle=DEI · Diario Emocional Inteligente',
                '-M', 'date=Noviembre 2026', '-M', 'toc-title=Contenido'], check=True)
d = Document(out)
sec = d.sections[0]
for se in d.sections:
    se.page_width = Cm(21); se.page_height = Cm(29.7)
    se.left_margin = se.right_margin = Cm(2); se.top_margin = se.bottom_margin = Cm(2)
width = sec.page_width - sec.left_margin - sec.right_margin
for st in d.styles:
    try:
        if st.type == 1 and st.font is not None:
            st.font.name = 'Calibri'
            rpr = st.element.get_or_add_rPr(); rf = rpr.find(qn('w:rFonts'))
            if rf is None: rf = OxmlElement('w:rFonts'); rpr.append(rf)
            for a in ('w:ascii', 'w:hAnsi', 'w:cs'): rf.set(qn(a), 'Calibri')
    except Exception: pass
for name, size, color in [('Title', 26, '1F3864'), ('Heading 1', 16, '1F3864'), ('Heading 2', 13, '2E74B5'), ('Heading 3', 12, '2E74B5')]:
    if name in d.styles:
        d.styles[name].font.size = Pt(size); d.styles[name].font.color.rgb = RGBColor.from_string(color)
for nm in ('Body Text', 'First Paragraph', 'Compact'):
    if nm in d.styles: d.styles[nm].font.size = Pt(10.5)
if 'Source Code' in d.styles: d.styles['Source Code'].font.size = Pt(8.5)
# tablas con bordes y encabezado sombreado
for t in d.tables:
    tblPr = t._tbl.tblPr
    b = OxmlElement('w:tblBorders')
    for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = OxmlElement(f'w:{e}'); el.set(qn('w:val'), 'single'); el.set(qn('w:sz'), '4'); el.set(qn('w:color'), 'A6A6A6'); b.append(el)
    tblPr.append(b)
    for c in t.rows[0].cells:
        sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), 'DEEAF6'); c._tc.get_or_add_tcPr().append(sh)
        for p in c.paragraphs:
            for r in p.runs: r.bold = True
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs: r.font.size = Pt(9.5)
# imágenes: las anchas van en una página horizontal propia; ninguna supera el área útil
import copy
from docx.enum.section import WD_ORIENT
body = d.element.body
final = body.sectPr
def make_sectpr(landscape):
    sp = copy.deepcopy(final)
    pg = sp.find(qn('w:pgSz'))
    if pg is None:
        pg = OxmlElement('w:pgSz'); sp.insert(0, pg)
    w, h = (Cm(29.7), Cm(21)) if landscape else (Cm(21), Cm(29.7))
    pg.set(qn('w:w'), str(int(w.twips))); pg.set(qn('w:h'), str(int(h.twips)))
    if landscape: pg.set(qn('w:orient'), 'landscape')
    elif pg.get(qn('w:orient')) is not None: del pg.attrib[qn('w:orient')]
    for t in sp.findall(qn('w:type')): sp.remove(t)
    return sp
port_w, port_h = Cm(17), Cm(23)
land_w, land_h = Cm(25.7), Cm(15.5)
paras = d.paragraphs
for i, para in enumerate(paras):
    blips = para._p.findall('.//' + qn('wp:inline'))
    if not blips: continue
    shape = [sh for sh in d.inline_shapes if sh._inline in blips][0]
    aspect = shape.width / shape.height
    wide = aspect > 1.45 and shape.width >= Cm(14)
    mw, mh = (land_w, land_h) if wide else (port_w, port_h)
    r = min(mw / shape.width, mh / shape.height, 10.0 if wide else 1.0)
    shape.width, shape.height = int(shape.width * r), int(shape.height * r)
    if not wide: continue
    # cerrar la sección vertical anterior (el título previo pasa a la página horizontal)
    start = para._p
    prev = start.getprevious()
    if prev is not None and prev.tag == qn('w:p'):
        sty = prev.find(qn('w:pPr') + '/' + qn('w:pStyle'))
        if sty is not None and sty.get(qn('w:val')).lower().startswith('heading'):
            start = prev
            prev = start.getprevious()
    prev_is_land = prev is not None and prev.find(qn('w:pPr') + '/' + qn('w:sectPr')) is not None and \
        prev.find(qn('w:pPr') + '/' + qn('w:sectPr') + '/' + qn('w:pgSz')).get(qn('w:orient')) == 'landscape'
    if not prev_is_land:
        brk = OxmlElement('w:p'); ppr = OxmlElement('w:pPr'); ppr.append(make_sectpr(False)); brk.append(ppr)
        start.addprevious(brk)
    last = para
    if i + 1 < len(paras) and paras[i + 1].style.name in ('Image Caption', 'Caption'):
        last = paras[i + 1]
    last._p.get_or_add_pPr().append(make_sectpr(True))
d.save(out)
