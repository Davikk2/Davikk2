import marshal
from pathlib import Path

SOURCE = r'''
# Hotfix isolado para a v38: somente o fluxo manual da aba Contas.
# A v37 substituiu adicionar_pdfs por uma versao incremental. Aqui restauramos
# apenas esse metodo original; como MainWindow.processar continua sendo o da v37
# e _v37_add_capture fica False, o metodo original dispara o processamento
# completo depois de copiar os anexos. Nenhuma outra funcao e alterada.
try:
    import views.main_window as _fix_mw

    _atual = _fix_mw.MainWindow.adicionar_pdfs
    _globais = getattr(_atual, '__globals__', {})
    _original = _globais.get('_v37_adicionar_original')
    if _original is not None:
        _fix_mw.MainWindow.adicionar_pdfs = _original
except Exception:
    try:
        _fix_mw.logger.exception('Falha ao aplicar hotfix isolado de anexos da aba Contas.')
    except Exception:
        pass
'''

code = compile(SOURCE, 'leitor_v38_attachment_fix.py', 'exec')
Path('leitor_v38_attachment_fix.bin').write_bytes(marshal.dumps(code))
print('compiled', len(marshal.dumps(code)))
