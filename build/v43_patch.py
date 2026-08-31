from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

old_gradient = "btn_img = make_round_image(bw, bh, 19, gradient=((104,91,226,255),(223,176,105,255)))"
new_gradient = "btn_img = make_round_image(bw, bh, 19, gradient=((11,108,126,255),(88,197,190,255)))"
if old_gradient not in text:
    raise RuntimeError('Gradiente antigo do botao Entrar nao encontrado')
text = text.replace(old_gradient, new_gradient, 1)

footer = "        footer = tk.Label(root, text='2026 | Desenvolvido por Erick', font=('Segoe UI', 10), bg=NAVY, fg=WHITE)\n        footer.place(relx=0.5, rely=0.952, anchor='center')\n\n"
if footer not in text:
    raise RuntimeError('Rodape Desenvolvido por Erick nao encontrado')
text = text.replace(footer, '', 1)

app.write_text(text, encoding='utf-8')
print('v43 patch applied: CC-colored login button + footer removed')
