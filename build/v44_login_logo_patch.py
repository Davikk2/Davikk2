from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# v44 parte da v43 aprovada e altera somente a tela de login:
# 1) troca o monograma CC pelo asset interligado fornecido pelo usuario;
# 2) remove o texto "Faça seu Login" sem deslocar o restante do formulario.

# Substitui apenas a etapa que desenha/cola o logo dentro de render_background.
render_start = text.find('        def render_background(w, h):\n')
icons_start = text.find("            icons=Image.new('RGBA',(W,H),(0,0,0,0))\n", render_start)
if render_start < 0 or icons_start < 0:
    raise RuntimeError('Bloco de fundo do login nao encontrado')

img_line_pos = text.find("            img=Image.new('RGBA',(W,H),(5,10,18,255))\n", render_start, icons_start)
if img_line_pos < 0:
    raise RuntimeError('Fundo solido da v43 nao encontrado')
img_line_end = img_line_pos + len("            img=Image.new('RGBA',(W,H),(5,10,18,255))\n")

logo_block = '''

            # Monograma CC interligado aprovado pelo usuario.
            # Asset transparente em alta resolucao; sem halo, fundo ou redesenho.
            try:
                logo_path=resource('data/cc_logo_user.webp')
                logo=Image.open(logo_path).convert('RGBA')
                # Mantem a mesma regiao visual da v43, com dimensao semelhante
                # a referencia aprovada na tela de login.
                target_w=int(W*0.28)
                target_h=int(H*0.34)
                logo.thumbnail((target_w,target_h), Image.Resampling.LANCZOS)
                lx=int(W*0.29-logo.width/2)
                ly=int(H*0.42-logo.height/2)
                img.alpha_composite(logo,(lx,ly))
            except Exception:
                pass

'''
text = text[:img_line_end] + logo_block + text[icons_start:]

# Remove a headline e o ponto colorido, mas conserva exatamente o espaco
# vertical ocupado pelo titulo para nao deslocar usuario/senha/botao.
old_title = """        title = tk.Frame(form, bg=RIGHT_BG)\n        title.pack(fill='x', pady=(0,26))\n        tk.Label(title, text='Faça seu Login', font=('Segoe UI', 27, 'bold'), bg=RIGHT_BG, fg=WHITE).pack(side='left')\n        tk.Label(title, text='.', font=('Segoe UI', 27, 'bold'), bg=RIGHT_BG, fg=DOT).pack(side='left')\n"""
new_title = """        title = tk.Frame(form, bg=RIGHT_BG, height=39)\n        title.pack(fill='x', pady=(0,26))\n        title.pack_propagate(False)\n"""
if old_title not in text:
    raise RuntimeError('Titulo Faça seu Login nao encontrado')
text = text.replace(old_title, new_title, 1)

app.write_text(text, encoding='utf-8')
print('v44 login patch applied: interlocked CC logo + title removed')
