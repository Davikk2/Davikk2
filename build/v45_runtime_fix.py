from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# Substitui TODO o trecho entre o fundo sólido e os ícones pelo novo asset.
render_start = text.find('        def render_background(w, h):\n')
img_line = "            img=Image.new('RGBA',(W,H),(5,10,18,255))\n"
img_pos = text.find(img_line, render_start)
icons_pos = text.find("            icons=Image.new('RGBA',(W,H),(0,0,0,0))", img_pos)
if render_start < 0 or img_pos < 0 or icons_pos < 0:
    raise RuntimeError('estrutura final do render_background nao encontrada')
img_end = img_pos + len(img_line)
logo_block = '''\n            # Novo CC interligado fornecido pelo usuario.\n            logo=Image.open(resource('data/cc_logo_user.png')).convert('RGBA')\n            maxw=int(W*0.28); maxh=int(H*0.34)\n            logo.thumbnail((maxw,maxh), Image.Resampling.LANCZOS)\n            lx=int(W*0.29-logo.width/2); ly=int(H*0.42-logo.height/2)\n            img.alpha_composite(logo,(lx,ly))\n\n'''
text = text[:img_end] + logo_block + text[icons_pos:]

# Remove por completo o texto e o ponto, preservando o frame e o espaçamento.
lines = text.splitlines(keepends=True)
out=[]
removed=False
for line in lines:
    if 'tk.Label(title' in line and 'Login' in line:
        removed=True
        continue
    if 'tk.Label(title' in line and "text='.'" in line:
        continue
    out.append(line)
text=''.join(out)
if not removed:
    raise RuntimeError('titulo do login nao encontrado')

# Validação final do trecho realmente executado no login.
login_start=text.find('    def show_login(self):')
login_end=text.find('    def login(self):', login_start)
login=text[login_start:login_end]
assert 'seu Login' not in login
assert "Image.open(resource('data/cc_logo_user.png'))" in login
assert 'draw_cc_logo(img, W, H)' not in login
assert 'paste_cc_logo(img, W, H)' not in login

app.write_text(text, encoding='utf-8')
print('runtime login fix aplicado e validado')
