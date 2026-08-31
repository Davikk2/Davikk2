from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# v43: botao Entrar com as cores do monograma CC.
old_gradient = "btn_img = make_round_image(bw, bh, 19, gradient=((104,91,226,255),(223,176,105,255)))"
new_gradient = "btn_img = make_round_image(bw, bh, 19, gradient=((11,108,126,255),(88,197,190,255)))"
if old_gradient in text:
    text = text.replace(old_gradient, new_gradient, 1)
elif new_gradient not in text:
    raise RuntimeError('Botao Entrar nao encontrado')

# v43: remove o rodape, se ainda existir.
footer = "        footer = tk.Label(root, text='2026 | Desenvolvido por Erick', font=('Segoe UI', 10), bg=NAVY, fg=WHITE)\n        footer.place(relx=0.5, rely=0.952, anchor='center')\n\n"
text = text.replace(footer, '', 1)

# v44: altera os comandos dos botoes por bloco, sem depender da formatacao inteira da linha.
def patch_button(block_start, block_end, origin):
    global text
    a = text.find(block_start)
    b = text.find(block_end, a)
    if a < 0 or b < 0:
        raise RuntimeError(f'Bloco {block_start} nao encontrado')
    block = text[a:b]
    old = 'command=self.add_files'
    new = f"command=lambda:self.add_files('{origin}')"
    if new in block:
        return
    if old not in block:
        raise RuntimeError(f'Botao Adicionar arquivos em {block_start} nao encontrado')
    block = block.replace(old, new, 1)
    text = text[:a] + block + text[b:]

patch_button('    def show_contas(self):', '    def show_conference(self):', 'contas')
patch_button('    def show_conference(self):', '    def change_comp(self):', 'conference')

# Substitui integralmente o metodo add_files. A string RAW preserva os \n como
# escapes no codigo gerado, em vez de inserir quebras de linha dentro de f-strings.
start = text.find('    def add_files(')
end = text.find('    def reprocess_folder(', start)
if start < 0 or end < 0:
    raise RuntimeError('Bloco add_files/reprocess_folder nao encontrado')

new_method = r'''    def add_files(self, origin='conference'):
        paths=[Path(x) for x in filedialog.askopenfilenames(title='Adicionar faturas',filetypes=[('PDF','*.pdf')])]
        if not paths:return
        try:
            res=self.service.process_files(self.active_comp,paths)
        except Exception as e:
            messagebox.showerror('Processamento',f'Falha ao processar os arquivos:\n{e}')
            return
        msg=(f"Processados: {res['processed']}\n"
             f"Reconhecidos: {res['recognized']}\n"
             f"Não reconhecidos: {res['unrecognized']}")
        errors=res.get('errors') or []
        if errors:
            preview='\n'.join(errors[:8])
            if len(errors)>8:
                preview += f"\n... e mais {len(errors)-8} erro(s)."
            msg += f"\n\nErros: {len(errors)}\n{preview}"
            messagebox.showwarning('Processamento concluído com erros',msg)
        else:
            messagebox.showinfo('Processamento',msg)
        if origin=='contas':
            self.show_contas()
        else:
            self.show_conference()
'''
text = text[:start] + new_method + text[end:]

app.write_text(text, encoding='utf-8')
print('v44 patch applied: attachment processing fixed and source remains valid')
