"""Genera el diagrama de datos (PlantUML) y el XMI 2.1 para Enterprise Architect."""
import glob, re, sys, uuid, html
from collections import OrderedDict

BACKEND, OUT = sys.argv[1], sys.argv[2]

# ---------------------------------------------------------------- modelo de datos
tables = OrderedDict()
for f in sorted(glob.glob(f'{BACKEND}/app/*/models/*.py')):
    s = open(f).read()
    t = re.search(r'__tablename__\s*=\s*"(\w+)"', s)
    cls = re.search(r'^class (\w+)\(', s, re.M).group(1)
    module = f.split('/app/')[1].split('/')[0]
    cols = []
    for m in re.finditer(r'^\s+(\w+)\s*(?::[^=]*)?=\s*(?:mapped_column|Column)\((.*?)\)\s*$', s, re.M | re.S):
        body = " ".join(m.group(2).split())
        fk = re.search(r'ForeignKey\("([^"]+)"', body)
        typ = re.match(r'\s*(\w+)(\([^)]*\))?', body)
        cols.append(dict(name=m.group(1), type=(typ.group(1) + (typ.group(2) or '')) if typ else '',
                         fk=fk.group(1) if fk else None, pk='primary_key=True' in body,
                         unique='unique=True' in body, nn='nullable=False' in body))
    tables[t.group(1)] = dict(cls=cls, module=module, cols=cols)

MODULE_COLORS = {'identity': '#E3F2FD', 'therapy': '#E8F5E9', 'entries': '#FFF8E1', 'analysis': '#FFF3E0',
                 'recommendations': '#F3E5F5', 'risk_alerts': '#FFEBEE', 'sessions': '#E0F7FA',
                 'notifications': '#F1F8E9', 'audit': '#ECEFF1', 'platform_consents': '#E8EAF6',
                 'administration': '#FBE9E7'}

lines = ['@startuml 04-modelo-datos', '!pragma layout smetana', 'title DEI - Modelo de datos (PostgreSQL)',
         'skinparam shadowing false', 'hide methods', 'hide stereotype', 'left to right direction']
by_mod = OrderedDict()
for tn, t in tables.items():
    by_mod.setdefault(t['module'], []).append(tn)
for mod, tns in by_mod.items():
    lines.append(f'package "{mod}" {MODULE_COLORS.get(mod, "")} {{')
    for tn in tns:
        lines.append(f'  entity "{tn}" as {tn} {{')
        for c in tables[tn]['cols']:
            mark = '*' if c['pk'] else ('+' if c['fk'] else ' ')
            extra = []
            if c['pk']: extra.append('PK')
            if c['fk']: extra.append('FK')
            if c['unique']: extra.append('UQ')
            if c['type'].startswith('Encrypted'): extra.append('cifrado')
            lines.append(f'    {mark}{c["name"]} : {c["type"]}' + (f'  <<{", ".join(extra)}>>' if extra else ''))
            if c['pk']: lines.append('    --')
        lines.append('  }')
    lines.append('}')
for tn, t in tables.items():
    for c in t['cols']:
        if c['fk']:
            target = c['fk'].split('.')[0]
            card = 'o|' if c['unique'] else 'o{'
            opt = '||' if c['nn'] else '|o'
            lines.append(f'{target} {opt}--{card} {tn} : {c["name"]}')
lines.append('@enduml')
open(f'{OUT}/plantuml/04-modelo-datos.puml', 'w').write('\n'.join(lines) + '\n')

# ---------------------------------------------------------------- XMI 2.1
def gid(*k):
    return 'EAID_' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'dei/' + '/'.join(k))).upper().replace('-', '_')

def esc(s):
    return html.escape(s, quote=True)

X = []
def w(s): X.append(s)

def pkg_open(name, key, doc=''):
    w(f'<packagedElement xmi:type="uml:Package" xmi:id="{gid("pkg", key)}" name="{esc(name)}">')
    if doc:
        w(f'<ownedComment xmi:type="uml:Comment" xmi:id="{gid("pkgdoc", key)}" body="{esc(doc)}"/>')

def comment(owner_key, body):
    w(f'<ownedComment xmi:type="uml:Comment" xmi:id="{gid("doc", owner_key)}" body="{esc(body)}"/>')

w('<?xml version="1.0" encoding="UTF-8"?>')
w('<xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1" '
  'xmlns:xmi="http://schema.omg.org/spec/XMI/2.1">')
w('<xmi:Documentation exporter="DEI docs generator" exporterVersion="1.0"/>')
w(f'<uml:Model xmi:type="uml:Model" name="DEI - Diario Emocional Inteligente" xmi:id="{gid("model")}" visibility="public">')

# primitive types
prims = sorted({re.sub(r'\(.*', '', c['type']) for t in tables.values() for c in t['cols']})
pkg_open('Tipos', 'types')
for p in prims:
    w(f'<packagedElement xmi:type="uml:PrimitiveType" xmi:id="{gid("type", p)}" name="{p}"/>')
w('</packagedElement>')

# ---- casos de uso
actors = {'pac': 'Paciente', 'psi': 'Psicólogo', 'adm': 'Administrador', 'ia': 'IA (Ollama / Gemini / Whisper)'}
ucs = OrderedDict([
    ('UC01', ('Registrarse e iniciar sesión', ['pac', 'psi'])), ('UC02', ('Recuperar contraseña', ['pac', 'psi'])),
    ('UC03', ('Aceptar consentimientos (informado, IA)', ['pac'])), ('UC04', ('Escribir entrada de texto', ['pac'])),
    ('UC05', ('Grabar entrada de voz', ['pac'])), ('UC06', ('Transcribir audio', ['ia'])),
    ('UC07', ('Analizar entrada con IA', ['pac', 'ia'])), ('UC08', ('Recibir ayuda en crisis', [])),
    ('UC09', ('Ver resumen semanal', ['pac', 'ia'])), ('UC10', ('Ver recomendaciones', ['pac'])),
    ('UC11', ('Solicitar vínculo con psicólogo', ['pac'])), ('UC12', ('Exportar o borrar mis datos', ['pac'])),
    ('UC13', ('Ver quién accedió a mis datos', ['pac'])),
    ('UC20', ('Aceptar / rechazar pacientes', ['psi'])), ('UC21', ('Ver entradas compartidas', ['psi'])),
    ('UC22', ('Atender alertas de riesgo', ['psi'])), ('UC23', ('Revisar recomendaciones de IA', ['psi'])),
    ('UC24', ('Gestionar sesiones y notas', ['psi'])), ('UC25', ('Ver insights del paciente', ['psi'])),
    ('UC30', ('Verificar psicólogos', ['adm'])), ('UC31', ('Activar / desactivar usuarios', ['adm'])),
    ('UC32', ('Configurar cadena de IA', ['adm'])), ('UC33', ('Gestionar líneas de crisis', ['adm'])),
    ('UC34', ('Ver estadísticas', ['adm'])),
])
includes = [('UC05', 'UC06')]
extends = [('UC04', 'UC07'), ('UC06', 'UC07'), ('UC07', 'UC08')]
pkg_open('Casos de uso', 'uc', 'Actores y casos de uso de DEI. Ver docs/arquitectura.md')
for k, n in actors.items():
    w(f'<packagedElement xmi:type="uml:Actor" xmi:id="{gid("actor", k)}" name="{esc(n)}"/>')
for k, (n, _) in ucs.items():
    inc = ''.join(f'<include xmi:type="uml:Include" xmi:id="{gid("inc", a, b)}" addition="{gid("uc", b)}"/>'
                  for a, b in includes if a == k)
    ext = ''.join(f'<extend xmi:type="uml:Extend" xmi:id="{gid("ext", a, b)}" extendedCase="{gid("uc", b)}"/>'
                  for b, a in extends if a == k)  # a extends b: extension is the extending case
    w(f'<packagedElement xmi:type="uml:UseCase" xmi:id="{gid("uc", k)}" name="{esc(k + " " + n)}">{inc}{ext}</packagedElement>')
for k, (n, acts) in ucs.items():
    for a in acts:
        aid = gid("assoc", a, k)
        w(f'<packagedElement xmi:type="uml:Association" xmi:id="{aid}" visibility="public">'
          f'<memberEnd xmi:idref="{gid("end", a, k, "a")}"/><memberEnd xmi:idref="{gid("end", a, k, "u")}"/>'
          f'<ownedEnd xmi:type="uml:Property" xmi:id="{gid("end", a, k, "a")}" type="{gid("actor", a)}" association="{aid}"/>'
          f'<ownedEnd xmi:type="uml:Property" xmi:id="{gid("end", a, k, "u")}" type="{gid("uc", k)}" association="{aid}"/>'
          '</packagedElement>')
w('</packagedElement>')

# ---- componentes y despliegue
comps = OrderedDict([
    ('app', ('App DEI (Flutter)', 'Cliente Android/iOS/Web. Riverpod, go_router, Dio.')),
    ('backend', ('dei_backend (FastAPI)', 'API REST, reglas clínicas, cadena de proveedores de IA.')),
    ('deiai', ('dei_ai (FastAPI)', 'Servicio de IA local: análisis con Ollama y transcripción con Faster-Whisper.')),
    ('ollama', ('Ollama', 'LLM local llama3.1:8b, puerto 11434.')),
    ('whisper', ('Servidor Whisper', 'API compatible con OpenAI /v1/audio/transcriptions.')),
    ('gemini', ('Gemini API', 'LLM en la nube, respaldo de la IA local.')),
    ('db', ('PostgreSQL', 'Base de datos con esquema administrado por Alembic.')),
    ('smtp', ('SMTP', 'Correo de códigos de recuperación.')),
])
backend_modules = ['identity', 'therapy', 'platform_consents', 'entries', 'analysis', 'recommendations',
                   'risk_alerts', 'sessions', 'notifications', 'dashboard', 'therapy_insights',
                   'administration', 'audit', 'health', 'shared.ai', 'shared.safety']
deps = [('app', 'backend', 'HTTPS + JWT'), ('backend', 'db', 'SQLAlchemy'), ('backend', 'ollama', 'HTTP /api/chat'),
        ('backend', 'gemini', 'google-genai'), ('backend', 'whisper', 'HTTP multipart'), ('backend', 'smtp', 'SMTP'),
        ('deiai', 'ollama', 'HTTP /api/chat'), ('backend', 'deiai', 'planificado')]
pkg_open('Componentes', 'comp')
for k, (n, d) in comps.items():
    w(f'<packagedElement xmi:type="uml:Component" xmi:id="{gid("comp", k)}" name="{esc(n)}">')
    comment('comp' + k, d)
    if k == 'backend':
        for m in backend_modules:
            w(f'<packagedElement xmi:type="uml:Component" xmi:id="{gid("comp", "be", m)}" name="{esc(m)}"/>')
    w('</packagedElement>')
for a, b, n in deps:
    w(f'<packagedElement xmi:type="uml:Dependency" xmi:id="{gid("dep", a, b)}" name="{esc(n)}" '
      f'client="{gid("comp", a)}" supplier="{gid("comp", b)}"/>')
w('</packagedElement>')

nodes = OrderedDict([('dev', ('Dispositivo del usuario', ['app'])),
                     ('thinkpad', ('ThinkPad (servidor de aplicación)', ['backend', 'db'])),
                     ('nitro', ('Nitro 5 (GPU, red local)', ['ollama', 'whisper', 'deiai'])),
                     ('cloud', ('Google Cloud', ['gemini']))])
pkg_open('Despliegue', 'deploy')
for k, (n, arts) in nodes.items():
    w(f'<packagedElement xmi:type="uml:Node" xmi:id="{gid("node", k)}" name="{esc(n)}">')
    for a in arts:
        w(f'<deployment xmi:type="uml:Deployment" xmi:id="{gid("depl", k, a)}" deployedArtifact="{gid("art", a)}"/>')
    w('</packagedElement>')
    for a in arts:
        w(f'<packagedElement xmi:type="uml:Artifact" xmi:id="{gid("art", a)}" name="{esc(comps[a][0])}">'
          f'<manifestation xmi:type="uml:Manifestation" xmi:id="{gid("man", a)}" utilizedElement="{gid("comp", a)}" supplier="{gid("comp", a)}" client="{gid("art", a)}"/>'
          '</packagedElement>')
w('</packagedElement>')

# ---- modelo de datos
pkg_open('Modelo de datos', 'data', 'Entidades SQLAlchemy de dei_backend. Generado desde app/*/models.')
for mod, tns in by_mod.items():
    pkg_open(mod, 'data/' + mod)
    for tn in tns:
        t = tables[tn]
        w(f'<packagedElement xmi:type="uml:Class" xmi:id="{gid("cls", tn)}" name="{t["cls"]}">')
        comment('cls' + tn, f'Tabla {tn}')
        for c in t['cols']:
            base = re.sub(r'\(.*', '', c['type'])
            lower = '1' if (c['nn'] or c['pk']) else '0'
            w(f'<ownedAttribute xmi:type="uml:Property" xmi:id="{gid("att", tn, c["name"])}" name="{c["name"]}" '
              f'visibility="public" type="{gid("type", base)}">'
              f'<lowerValue xmi:type="uml:LiteralInteger" xmi:id="{gid("lv", tn, c["name"])}" value="{lower}"/>'
              f'<upperValue xmi:type="uml:LiteralUnlimitedNatural" xmi:id="{gid("uv", tn, c["name"])}" value="1"/>'
              '</ownedAttribute>')
        w('</packagedElement>')
    w('</packagedElement>')
for tn, t in tables.items():
    for c in t['cols']:
        if not c['fk']:
            continue
        target = c['fk'].split('.')[0]
        aid = gid('fk', tn, c['name'])
        many = '1' if c['unique'] else '*'
        tlow = '1' if c['nn'] else '0'
        w(f'<packagedElement xmi:type="uml:Association" xmi:id="{aid}" name="{c["name"]}" visibility="public">'
          f'<memberEnd xmi:idref="{gid("fkend", tn, c["name"], "src")}"/><memberEnd xmi:idref="{gid("fkend", tn, c["name"], "dst")}"/>'
          f'<ownedEnd xmi:type="uml:Property" xmi:id="{gid("fkend", tn, c["name"], "src")}" type="{gid("cls", tn)}" association="{aid}">'
          f'<lowerValue xmi:type="uml:LiteralInteger" xmi:id="{gid("fkl", tn, c["name"], "s")}" value="0"/>'
          f'<upperValue xmi:type="uml:LiteralUnlimitedNatural" xmi:id="{gid("fku", tn, c["name"], "s")}" value="{many}"/></ownedEnd>'
          f'<ownedEnd xmi:type="uml:Property" xmi:id="{gid("fkend", tn, c["name"], "dst")}" type="{gid("cls", target)}" association="{aid}">'
          f'<lowerValue xmi:type="uml:LiteralInteger" xmi:id="{gid("fkl", tn, c["name"], "d")}" value="{tlow}"/>'
          f'<upperValue xmi:type="uml:LiteralUnlimitedNatural" xmi:id="{gid("fku", tn, c["name"], "d")}" value="1"/></ownedEnd>'
          '</packagedElement>')
w('</packagedElement>')

w('</uml:Model>')
w('</xmi:XMI>')
open(f'{OUT}/enterprise-architect/dei-modelo.xmi', 'w', encoding='utf-8').write('\n'.join(X) + '\n')
print(len(tables), 'tablas')
