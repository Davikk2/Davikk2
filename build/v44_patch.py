from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# Faz cada botao de anexar atualizar a propria aba ao final do processamento.
old_contas = "tk.Button(bar,text='Adicionar arquivos',command=self.add_files,bg=ACCENT2,fg='white',relief='flat',padx=14,pady=8).pack(side='left')"
new_contas = "tk.Button(bar,text='Adicionar arquivos',command=lambda:self.add_files('contas'),bg=ACCENT2,fg='white',relief='flat',padx=14,pady=8).pack(side='left')"
if old_contas not in text:
    raise RuntimeError('Botao Adicionar arquivos da aba Contas nao encontrado')
text = text.replace(old_contas, new_contas, 1)

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
        # Atualiza imediatamente a tela de onde o usuario iniciou o anexo.
        if origin=='contas':
            self.show_contas()
        else:
            self.show_conference()
'''
if old_method not in text:
    raise RuntimeError('Metodo add_files original nao encontrado')
text = text.replace(old_method, new_method, 1)

app.write_text(text, encoding='utf-8')
print('v44 patch applied: attachments process and refresh the originating tab')
