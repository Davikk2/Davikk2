from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# v43: botao Entrar com as cores do monograma CC.
old_gradient = "btn_img = make_round_image(bw, bh, 19, gradient=((104,91,226,255),(223,176,105,255)))"
new_gradient = "btn_img = make_round_image(bw, bh, 19, gradient=((11,108,126,255),(88,197,190,255)))"
if old_gradient not in text:
    raise RuntimeError('Gradiente antigo do botao Entrar nao encontrado')
text = text.replace(old_gradient, new_gradient, 1)

# v43: remove o rodape.
footer = "        footer = tk.Label(root, text='2026 | Desenvolvido por Erick', font=('Segoe UI', 10), bg=NAVY, fg=WHITE)\n        footer.place(relx=0.5, rely=0.952, anchor='center')\n\n"
if footer not in text:
    raise RuntimeError('Rodape Desenvolvido por Erick nao encontrado')
text = text.replace(footer, '', 1)

# v44: o botao da aba Contas deve processar e atualizar a propria aba.
old_contas = "tk.Button(bar,text='Adicionar arquivos',command=self.add_files,bg=ACCENT2,fg='white',relief='flat',padx=14,pady=8).pack(side='left')"
new_contas = "tk.Button(bar,text='Adicionar arquivos',command=lambda:self.add_files('contas'),bg=ACCENT2,fg='white',relief='flat',padx=14,pady=8).pack(side='left')"
if old_contas not in text:
    raise RuntimeError('Botao Adicionar arquivos da aba Contas nao encontrado')
text = text.replace(old_contas, new_contas, 1)

# Conferencia continua atualizando a propria tela.
old_conf = "tk.Button(top,text='Adicionar arquivos',command=self.add_files,bg=ACCENT2,fg='white',relief='flat',padx=12,pady=7).pack(side='left',padx=5)"
new_conf = "tk.Button(top,text='Adicionar arquivos',command=lambda:self.add_files('conference'),bg=ACCENT2,fg='white',relief='flat',padx=12,pady=7).pack(side='left',padx=5)"
if old_conf not in text:
    raise RuntimeError('Botao Adicionar arquivos da Conferencia nao encontrado')
text = text.replace(old_conf, new_conf, 1)

old_method = '''    def add_files(self):
        paths=[Path(x) for x in filedialog.askopenfilenames(title='Adicionar faturas',filetypes=[('PDF','*.pdf')])]
        if not paths:return
        res=self.service.process_files(self.active_comp,paths);messagebox.showinfo('Processamento',f"Processados: {res['processed']}\nReconhecidos: {res['recognized']}\nNão reconhecidos: {res['unrecognized']}");self.show_conference()
'''
new_method = '''    def add_files(self, origin='conference'):
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
            if len(errors)>8:preview += f"\n... e mais {len(errors)-8} erro(s)."
            msg += f"\n\nErros: {len(errors)}\n{preview}"
            messagebox.showwarning('Processamento concluído com erros',msg)
        else:
            messagebox.showinfo('Processamento',msg)
        if origin=='contas':
            self.show_contas()
        else:
            self.show_conference()
'''
if old_method not in text:
    raise RuntimeError('Metodo add_files original nao encontrado')
text = text.replace(old_method, new_method, 1)

app.write_text(text, encoding='utf-8')
print('v43/v44 patch applied: login visual + attachment processing refresh fix')
