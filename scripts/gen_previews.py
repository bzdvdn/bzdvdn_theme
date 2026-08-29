#!/usr/bin/env python3
import html, pathlib, subprocess

ASSETS = pathlib.Path('/home/bzdv/PAT_PROJECTS/BZDVDN_THEME/assets')
ROOT = pathlib.Path('/home/bzdv/PAT_PROJECTS/BZDVDN_THEME')

# theme colors
C = dict(
    comment='#503f50', kw='#4ADE80', fn='#00d4f9', type='#5877f4',
    str='#bbff00', num='#F472B6', op='#1087f0', opr='#7A8A84',
    var='#D4D4D4', this='#F472B6', self='#a340a3', prop='#86EFAC',
    param='#fdfb5d', deco='#FB7185', module='#5877f4', tag='#5699f0',
    anchor='#FDBA74', prim='#99F6E4', arrow='#4ADE80',
)

FONT = "'Ubuntu Mono','DejaVu Sans Mono',monospace"

def span(text, cls):
    if not cls:
        return html.escape(text)
    c = C[cls]
    bold = cls in ('kw','fn','type','op','this','self','param','tag','module','arrow')
    em = cls in ('comment','deco')
    style = f'color:{c};'
    if bold: style += 'font-weight:bold;'
    if em: style += 'font-style:italic;'
    return f'<span style="{style}">{html.escape(text)}</span>'

def line(tokens, num):
    if isinstance(tokens, str):
        tokens = [(tokens, '')]
    body = ''.join(span(t, c) for t, c in tokens)
    return (f'<div style="display:flex;height:21px;line-height:21px;white-space:pre;">'
            f'<div style="width:44px;flex:none;color:#515962;text-align:right;padding-right:8px;'
            f'background:#141414;user-select:none;">{num}</div>'
            f'<div style="flex:none;color:transparent;background:#141414">  </div>'
            f'<div style="color:#e0e2ea;background:#141414">{body}</div></div>')

def render(name, tab, lines):
    body = ''.join(line(l, i) for i, l in enumerate(lines, 1))
    # emulate editor sentinel space, border-box root paint
    h = 21 * len(lines) + 35 + 4
    html_str = f'''<!doctype html><html><head><meta charset="utf-8">
<style>
  *{{margin:0;padding:0;box-sizing:border-box;}}
  html,body{{background:#0e0e0e;}}
  .tabs{{display:flex;height:35px;background:#0e0e0e;align-items:stretch;}}
  .tab{{display:flex;align-items:center;padding:0 14px;font:12px {FONT};color:#6E7681;
        border-top:2px solid transparent;background:#0e0e0e;white-space:nowrap;}}
  .tab.active{{background:#141414;color:#e0e2ea;border-top-color:#4AEDC4;}}
  .tab .dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px;background:#4AEDC4;}}
  .mono{{font:13px {FONT};}}
</style></head><body>
<div class="tabs">
  <div class="tab active"><span class="dot"></span>{html.escape(tab)}</div>
  <div class="tab">README.md</div>
</div>
<div class="mono">
{body}
</div>
</body></html>'''
    out_html = ASSETS / (name + '.html')
    out_png = ASSETS / (name + '.png')
    out_html.write_text(html_str)
    subprocess.run([
        'chromium', '--headless=new', '--no-sandbox', '--disable-gpu',
        '--force-device-scale-factor=2',
        f'--window-size=860,{h*2}',
        f'--screenshot={out_png}',
        out_html.resolve().as_uri(),
    ], capture_output=True)
    print('rendered', out_png.name)
    from PIL import Image
    im = Image.open(out_png).convert('RGB')
    px = im.load()
    w, h = im.size
    bg = (14, 14, 14)
    xs, ys = [], []
    for y in range(h):
        for x in range(0, w, 2):
            if px[x, y] != bg:
                xs.append(x); ys.append(y)
    if xs:
        l, t, r, b = min(xs), min(ys), max(xs), max(ys)
        pad = 14
        l = max(0, l - pad); t = max(0, t - pad)
        r = min(w, r + pad); b = min(h, b + pad)
        im.crop((l, t, r, b)).save(out_png)
        print('trimmed', out_png.name, '->', im.crop((l, t, r, b)).size)

# ---------------- GO ----------------
go = [
    "package users",
    "",
    'import "database/sql"',
    "",
    [('// User represents a user in the system', 'comment')],
    [('type ', 'kw'), ('User', 'type'), (' struct', 'kw'), (' {', '')],
    [('    ID   ', ''), ('int64', 'type')],
    [('    Name ', ''), ('string', 'type')],
    [('}', '')],
    "",
    [('func (', 'kw'), ('u', 'self'), (' *', ''), ('User', 'type'), (') ', ''), ('Full', 'fn'),
     ('() ', ''), ('string', 'type'), (' {', '')],
    [('    return ', 'kw'), ('u', ''), ('.', ''), ('Name', 'prop'), (' ', ''), ('+', 'op'),
     (' ', ''), ('" #"', 'str'), (' ', ''), ('+', 'op'), (' ', ''), ('fmt', 'module'),
     ('.', ''), ('Sprint', 'fn'), ('(u.ID)', '')],
    [('}', '')],
    "",
    [('func ', 'kw'), ('New', 'fn'), ('() *', ''), ('User', 'type'), (' {', '')],
    [('    return ', 'kw'), ('&', ''), ('User', 'type'), ('{', ''), ('ID', 'prop'),
     (': ', ''), ('1', 'num'), ('}', '')],
    [('}', '')],
]
render('preview-go', 'main.go', go)

# ---------------- PYTHON ----------------
py = [
    [('import ', 'kw'), ('json', 'module')],
    "",
    [('class ', 'kw'), ('User', 'type'), (':', '')],
    [('    def ', 'kw'), ('__init__', 'fn'), ('(self', 'self'), (', ', ''), ('name', 'param'),
     (': ', ''), ('str', 'type'), (') ', ''), ('->', 'arrow'), (' ', ''), ('None', 'num'), (':', '')],
    [('        self', 'self'), ('.name = ', 'prop'), ('name', 'var')],
    "",
    [('    @property', 'deco')],
    [('    def ', 'kw'), ('upper_name', 'fn'), ('(self)', 'self'), (' -> ', 'arrow'),
     (' ', ''), ('str', 'type'), (':', '')],
    [('        return ', 'kw'), ('self', 'self'), ('.name', 'prop'),
     ('.', ''), ('upper', 'fn'), ('()', '')],
    "",
    [('    # build a user from raw data', 'comment')],
    [('    @classmethod', 'deco')],
    [('    def ', 'kw'), ('from_dict', 'fn'), ('(cls', 'self'), (', ', ''), ('data', 'param'),
     (': ', ''), ('dict', 'type'), (') ', ''), ('->', 'arrow'), (' ', ''), ('"User"', 'str'),
     (':', '')],
    [('        return ', 'kw'), ('cls', 'self'), ('(', ''), ('**', 'op'), ('data', 'var'), (')', '')],
]
render('preview-python', 'models.py', py)

# ---------------- TS ----------------
ts = [
    [('import { ', 'kw'), ('getUser', 'var'), (' } from ', 'kw'), ('"./api"', 'str'), (';', '')],
    "",
    [('const ', 'kw'), ('cache', 'var'), (' = ', ''), ('new ', 'kw'), ('Map', 'type'),
     ('<', ''), ('string', 'prim'), (', ', ''), ('User', 'type'), ('>', ''), (';', '')],
    "",
    [('async ', 'kw'), ('function ', 'kw'), ('loadUser', 'fn'), ('(', ''), ('id', 'param'),
     (': ', ''), ('number', 'prim'), ('): ', ''), ('Promise', 'type'), ('<', ''),
     ('User', 'type'), (' | ', ''), ('null', 'num'), ('>', ''), (' {', '')],
    [('  this', 'this'), ('.logger', 'prop'), ('?.', 'op'), ('info', 'fn'),
     ('(`', 'str'), ('fetch user ', 'str'), ('${', 'arrow'), ('id', 'var'), ('}', 'arrow'),
     ('`)', 'str'), (';', '')],
    "",
    [('  return ', 'kw'), ('cache', 'var'), ('.', ''), ('get', 'fn'), ('(', ''), ('id', 'var'),
     (') ', ''), ('??', 'op'), (' ', ''), ('fallback', 'var'), (';', '')],
    [('}', '')],
    "",
    [('// Cache healthy? check, then reload', 'comment')],
    [('if ', 'kw'), ('(', ''), ('!', 'op'), ('cache', 'var'), ('.size', 'prop'), (') ', ''),
     ('await ', 'kw'), ('loadUser', 'fn'), ('(', ''), ('1', 'num'), (');', '')],
]
render('preview-ts', 'api.ts', ts)

# ---------------- YAML ----------------
ya = [
    [('service', 'tag'), (':', ''), (' ', ''), ('api', 'str')],
    [('image', 'tag'), (':', ''), (' ', ''), ('!reference', 'tag'), (' [', ''),
     ('.build', 'tag'), (', ', ''), ('image', 'str'), (']', '')],
    [('replicas', 'tag'), (':', ''), (' ', ''), ('&rep', 'anchor'), (' ', ''), ('3', 'num')],
    [('env', 'tag'), (':', '')],
    [('  HOST', 'tag'), (':', ''), (' ', ''), ('*rep', 'anchor'),
     ('  # override host', 'comment')],
    [('  PORT', 'tag'), (':', ''), (' ', ''), ('8080', 'num')],
    "",
    [('volumes', 'tag'), (':', '')],
    [('  - ', ''), ('name', 'tag'), (':', ''), (' ', ''), ('data', 'str')],
    [('    path', 'tag'), (':', ''), (' ', ''), ('/var/lib/data', 'str')],
]
render('preview-yaml', 'values.yaml', ya)