from pathlib import Path
import shutil

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# Base: v43 aprovada. Alteração única: substituir o CC do login
# pelo asset mesclado fornecido pelo usuário. Nenhum outro texto,
# posição, cor, controle ou comportamento deve mudar.

src_logo = Path('../build/assets/cc_logo_mesclado.png')
dst_logo = Path('data/cc_logo_mesclado.png')
if not src_logo.exists():
    raise RuntimeError('Asset do CC mesclado nao encontrado')
dst_logo.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(src_logo, dst_logo)

render_start = text.find('        def render_background(w, h):\n')
icons_start = text.find("            icons=Image.new('RGBA',(W,H),(0,0,0,0))\n", render_start)
if render_start < 0 or icons_start < 0:
    raise RuntimeError('Bloco render_background da v43 nao encontrado')

img_line = "            img=Image.new('RGBA',(W,H),(5,10,18,255))\n"
img_pos = text.find(img_line, render_start, icons_start)
if img_pos < 0:
    raise RuntimeError('Fundo solido da v43 nao encontrado')
img_end = img_pos + len(img_line)

new_logo = '''

            # CC mesclado fornecido pelo usuário, preservado como asset PNG.
            try:
                logo_path = resource('data/cc_logo_mesclado.png')
                logo = Image.open(logo_path).convert('RGBA')
                # Mantém a mesma região visual ocupada pelo logo da v43.
                target_w = int(W * 0.285)
                target_h = int(H * 0.36)
                logo.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
                lx = int(W * 0.29 - logo.width / 2)
                ly = int(H * 0.42 - logo.height / 2)
                img.alpha_composite(logo, (lx, ly))
            except Exception:
                pass

'''

# Remove qualquer bloco anterior de desenho do logo entre a criação do fundo
# e os ícones, substituindo somente por este asset.
text = text[:img_end] + new_logo + text[icons_start:]

app.write_text(text, encoding='utf-8')
print('v43 logo-only patch applied')
