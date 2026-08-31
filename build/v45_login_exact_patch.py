from pathlib import Path
import base64

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

LOGO_B64 = "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..." 

# Write exact approved user logo asset into project data.
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)
(data_dir / 'cc_logo_user.png').write_bytes(base64.b64decode(LOGO_B64))

# Replace only logo draw call inside final render_background.
start = text.find('        def render_background(w, h):\n')
end = text.find('            icons=Image.new', start)
if start < 0 or end < 0:
    raise RuntimeError('render_background final nao encontrado')
segment = text[start:end]
if 'draw_cc_logo(img, W, H)' not in segment and 'paste_cc_logo(img, W, H)' not in segment:
    raise RuntimeError('chamada do logo antigo nao encontrada')
segment = segment.replace('            draw_cc_logo(img, W, H)\n', '''            try:\n                logo=Image.open(resource('data/cc_logo_user.png')).convert('RGBA')\n                maxw=int(W*0.28); maxh=int(H*0.34)\n                logo.thumbnail((maxw,maxh), Image.Resampling.LANCZOS)\n                lx=int(W*0.29-logo.width/2); ly=int(H*0.42-logo.height/2)\n                img.alpha_composite(logo,(lx,ly))\n            except Exception:\n                pass\n''')
segment = segment.replace('            paste_cc_logo(img, W, H)\n', '''            try:\n                logo=Image.open(resource('data/cc_logo_user.png')).convert('RGBA')\n                maxw=int(W*0.28); maxh=int(H*0.34)\n                logo.thumbnail((maxw,maxh), Image.Resampling.LANCZOS)\n                lx=int(W*0.29-logo.width/2); ly=int(H*0.42-logo.height/2)\n                img.alpha_composite(logo,(lx,ly))\n            except Exception:\n                pass\n''')
text = text[:start] + segment + text[end:]

# Remove headline and purple dot completely while preserving spacer.
lines = text.splitlines(keepends=True)
out=[]
removed_title=False
for line in lines:
    if 'tk.Label(title' in line and 'Login' in line:
        removed_title=True
        continue
    if 'tk.Label(title' in line and "text='.'" in line:
        continue
    out.append(line)
text=''.join(out)
if not removed_title:
    raise RuntimeError('headline do login nao encontrada')

# Hard validations: build must stop if visual change is not really present.
login_start=text.find('    def show_login(self):')
login_end=text.find('    def login(self):', login_start)
login=text[login_start:login_end]
if 'Faça seu Login' in login or 'Faca seu Login' in login or 'seu Login' in login:
    raise RuntimeError('titulo ainda presente no login final')
if "cc_logo_user.png" not in login:
    raise RuntimeError('novo asset CC nao esta sendo carregado no login final')
if 'draw_cc_logo(img, W, H)' in login or 'paste_cc_logo(img, W, H)' in login:
    raise RuntimeError('logo antigo ainda esta sendo desenhado no login final')

app.write_text(text, encoding='utf-8')
print('v45 final login patch applied and validated')
