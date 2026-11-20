import re, subprocess, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Emu
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
src, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src, encoding='utf-8').read()
s = re.sub(r'\[([^\]]+)\]\((?!https?:)[^)]*\.md[^)]*\)', r'\1', s)       # enlaces entre documentos
s = re.sub(r'\[`?diagramas/`?\]\(diagramas/\)', '`diagramas/`', s)
s = re.sub(r'^# .*\n', '', s, count=1)
md = out + '.md'
open(md, 'w', encoding='utf-8').write(s)
subprocess.run(['pandoc', md, '-f', 'gfm', '-o', out, '--toc', '--toc-depth=2', 
                '--resource-path=.', '-M', f'title={title}', '-M', 'subtitle=DEI · Diario Emocional Inteligente',
                '-M', 'date=Noviembre 2026', '-M', 'toc-title=Contenido'], check=True)
d = Document(out)
sec = d.sections[0]
for se in d.sections:
    se.page_width = Cm(21); se.page_height = Cm(29.7)
    se.left_margin = se.right_margin = Cm(2); se.top_margin = se.bottom_margin = Cm(2)
def style_of(n):
    for st in d.styles:
        if st.name and st.name.lower() == n.lower(): return st
    return None
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
    st = style_of(name)
    if st is not None:
        st.font.size = Pt(size); st.font.color.rgb = RGBColor.from_string(color)
for nm in ('Body Text', 'First Paragraph', 'Compact'):
    if style_of(nm) is not None: style_of(nm).font.size = Pt(10.5)
if style_of('Source Code') is not None: style_of('Source Code').font.size = Pt(8.5)
# anchos de columna según el contenido
def fit_columns(t, total):
    ncol = len(t.columns)
    lens = [0.0] * ncol
    for row in t.rows:
        for i, c in enumerate(row.cells[:ncol]):
            txt = c.text
            longest = max((len(w) for w in txt.split()), default=1)
            lens[i] = max(lens[i], min(len(txt), 60) * 0.7 + longest * 0.3)
    lens = [max(l, 8) for l in lens]
    s_ = sum(lens)
    widths = [int(total * l / s_) for l in lens]
    tblPr = t._tbl.tblPr
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
    tw = tblPr.find(qn('w:tblW'))
    if tw is None:
        tw = OxmlElement('w:tblW'); tblPr.append(tw)
    tw.set(qn('w:type'), 'dxa'); tw.set(qn('w:w'), str(int(Emu(total).twips)))
    grid = t._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn('w:gridCol'))):
        gc.set(qn('w:w'), str(int(Emu(widths[i]).twips)))
    for row in t.rows:
        for i, c in enumerate(row.cells[:ncol]):
            c.width = Emu(widths[i])
for t in d.tables:
    fit_columns(t, int(Cm(17)))
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
    mw, mh = (land_w, land_h) if wide else (port_w, Cm(13) if aspect < 0.8 else port_h)
    r = min(mw / shape.width, mh / shape.height, 10.0 if wide else 1.0)
    shape.width, shape.height = int(shape.width * r), int(shape.height * r)
    if not wide: continue
    # cerrar la sección vertical anterior (el título previo pasa a la página horizontal)
    BM = (qn('w:bookmarkStart'), qn('w:bookmarkEnd'))
    def prev_p(el):
        p_ = el.getprevious()
        while p_ is not None and p_.tag in BM:
            el = p_
            p_ = p_.getprevious()
        return p_
    start = para._p
    prev = prev_p(start)
    moved = 0
    while prev is not None and prev.tag == qn('w:p') and moved < 3 \
            and prev.find(qn('w:pPr') + '/' + qn('w:sectPr')) is None:
        st_el = prev.find(qn('w:pPr') + '/' + qn('w:pStyle'))
        is_head = st_el is not None and st_el.get(qn('w:val')).lower().startswith('heading')
        text = ''.join(t.text or '' for t in prev.iter(qn('w:t')))
        is_list = prev.find(qn('w:pPr') + '/' + qn('w:numPr')) is not None
        if not (is_head or (len(text) < 300 and not is_list and prev.find('.//' + qn('wp:inline')) is None and moved == 0)):
            break
        start = prev
        while start.getprevious() is not None and start.getprevious().tag in BM:
            start = start.getprevious()
        prev = prev_p(start)
        moved += 1
        if is_head and st_el.get(qn('w:val')).lower() in ('heading1', 'heading 1'):
            break
    prev_is_land = prev is not None and prev.find(qn('w:pPr') + '/' + qn('w:sectPr')) is not None and \
        prev.find(qn('w:pPr') + '/' + qn('w:sectPr') + '/' + qn('w:pgSz')).get(qn('w:orient')) == 'landscape'
    if not prev_is_land:
        brk = OxmlElement('w:p'); ppr = OxmlElement('w:pPr'); ppr.append(make_sectpr(False)); brk.append(ppr)
        start.addprevious(brk)
    last = para
    if i + 1 < len(paras) and paras[i + 1].style.name in ('Image Caption', 'Caption'):
        last = paras[i + 1]
    last._p.get_or_add_pPr().append(make_sectpr(True))
# cada capítulo en página nueva
style_of('Heading 1').paragraph_format.page_break_before = True
d.save(out)
# pedir a Word que actualice el índice al abrir
import zipfile, shutil, os
tmp = out + '.tmp'
with zipfile.ZipFile(out) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == 'word/settings.xml' and b'updateFields' not in data:
            data = data.replace(b'</w:settings>', b'<w:updateFields w:val="true"/></w:settings>')
        zout.writestr(item, data)
shutil.move(tmp, out)
