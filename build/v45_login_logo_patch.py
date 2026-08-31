from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# Esta correção parte da v43 aprovada e altera SOMENTE dois pontos da tela de login:
# 1) o monograma grande CC passa a usar o asset mesclado fornecido pelo usuário;
# 2) o título "Faça seu Login" é removido mantendo o espaço/formulário estável.

# --- Logo grande da tela de login -------------------------------------------------
render_start = text.find('        def render_background(w, h):')
render_end = text.find('        def redraw():', render_start)
if render_start < 0 or render_end < 0:
    raise RuntimeError('render_background da tela de login não encontrado')

render = text[render_start:render_end]
old_logo_line = '            draw_cc_logo(img, W, H)\n'
if old_logo_line not in render:
    raise RuntimeError('Chamada do logo antigo não encontrada na v43')

new_logo_block = '''            # CC mesclado fornecido pelo usuário. Asset real, sem redesenho.\n            try:\n                logo_path = resource('data/cc_logo_user.png')\n                logo = Image.open(logo_path).convert('RGBA')\n                # Renderiza no canvas 2x e reduz junto com o fundo, preservando nitidez.\n                max_w = int(W * 0.30)\n                max_h = int(H * 0.36)\n                logo.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)\n                lx = int(W * 0.29 - logo.width / 2)\n                ly = int(H * 0.42 - logo.height / 2)\n                img.alpha_composite(logo, (lx, ly))\n            except Exception:\n                pass\n'''
render = render.replace(old_logo_line, new_logo_block, 1)
text = text[:render_start] + render + text[render_end:]

# --- Título "Faça seu Login" ------------------------------------------------------
lines = text.splitlines(keepends=True)
out = []
i = 0
changed_title = False
while i < len(lines):
    line = lines[i]
    if 'title = tk.Frame(form, bg=RIGHT_BG)' in line:
        indent = line[:len(line) - len(line.lstrip())]
        # Confirma que estamos no bloco correto antes de substituir.
        lookahead = ''.join(lines[i:i+6])
        if 'tk.Label(title' in lookahead and 'Login' in lookahead:
            out.append(indent + "title = tk.Frame(form, bg=RIGHT_BG, height=39)\n")
            out.append(indent + "title.pack(fill='x', pady=(0,26))\n")
            out.append(indent + "title.pack_propagate(False)\n")
            # Pula o frame original, o pack e as duas labels do título/ponto.
            i += 1
            while i < len(lines):
                candidate = lines[i]
                if candidate.strip() == '':
                    out.append(candidate)
                    i += 1
                    break
                if ('title.pack' in candidate or 'tk.Label(title' in candidate):
                    i += 1
                    continue
                break
            changed_title = True
            continue
    out.append(line)
    i += 1

if not changed_title:
    raise RuntimeError('Bloco visual do título de login não encontrado')

text = ''.join(out)

# Validações para evitar gerar novamente um executável visualmente antigo.
if 'Faça seu Login' in text or 'FaÃ§a seu Login' in text:
    raise RuntimeError('O texto Faça seu Login ainda existe após o patch')
if "resource('data/cc_logo_user.png')" not in text:
    raise RuntimeError('O novo asset CC não foi ligado ao render_background')

app.write_text(text, encoding='utf-8')
print('v45 login patch applied: exact user CC asset + login headline removed')
