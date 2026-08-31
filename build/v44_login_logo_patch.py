from pathlib import Path
import re

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# v44 parte EXATAMENTE da v43 aprovada e altera somente a tela de login:
# 1) substitui o monograma antigo pelo CC interligado da referencia do usuario;
# 2) remove o titulo do login mantendo o restante do formulario na mesma posicao.

render_start = text.find('        def render_background(w, h):\n')
icons_start = text.find("            icons=Image.new('RGBA',(W,H),(0,0,0,0))\n", render_start)
if render_start < 0 or icons_start < 0:
    raise RuntimeError('Bloco de fundo do login nao encontrado')

img_line = "            img=Image.new('RGBA',(W,H),(5,10,18,255))\n"
img_line_pos = text.find(img_line, render_start, icons_start)
if img_line_pos < 0:
    raise RuntimeError('Fundo solido da v43 nao encontrado')
img_line_end = img_line_pos + len(img_line)

logo_block = '''

            # CC interligado/mesclado aprovado para a tela de login.
            logo_layer=Image.new('RGBA',(W,H),(0,0,0,0))
            combined_cx=int(W*0.29)
            cy=int(H*0.42)
            r=int(min(W,H)*0.16)
            stroke=max(10,int(r*0.38))
            inner=max(1,r-stroke)
            center_gap=int(r*0.95)
            cx1=combined_cx-center_gap//2
            cx2=combined_cx+center_gap//2

            def c_mask(cx):
                m=Image.new('L',(W,H),0)
                md=ImageDraw.Draw(m)
                md.ellipse((cx-r,cy-r,cx+r,cy+r),fill=255)
                md.ellipse((cx-inner,cy-inner,cx+inner,cy+inner),fill=0)
                half_gap=int(r*0.355)
                md.rectangle((cx,cy-half_gap,cx+r+stroke,cy+half_gap),fill=0)
                return m

            left_mask=c_mask(cx1)
            right_mask=c_mask(cx2)

            def gradient_layer(mask, c0, c1):
                layer=Image.new('RGBA',(W,H),(0,0,0,0))
                ld=ImageDraw.Draw(layer)
                x0=min(cx1,cx2)-r
                x1=max(cx1,cx2)+r
                span=max(1,x1-x0)
                for x in range(max(0,x0),min(W,x1+1)):
                    t=(x-x0)/span
                    col=tuple(int(c0[i]*(1-t)+c1[i]*t) for i in range(3))
                    ld.line((x,max(0,cy-r),x,min(H,cy+r)),fill=(*col,255))
                layer.putalpha(mask)
                return layer

            left_logo=gradient_layer(left_mask,(7,108,135),(24,151,164))
            right_logo=gradient_layer(right_mask,(44,166,174),(76,190,187))
            logo_layer.alpha_composite(left_logo)
            logo_layer.alpha_composite(right_logo)

            overlap=ImageChops.multiply(left_mask,right_mask)
            overlap_layer=Image.new('RGBA',(W,H),(0,0,0,0))
            od=ImageDraw.Draw(overlap_layer)
            top=max(0,cy-r); bottom=min(H,cy+r); span_y=max(1,bottom-top)
            for y in range(top,bottom+1):
                t=(y-top)/span_y
                c0=(37,56,72); c1=(28,48,62)
                col=tuple(int(c0[i]*(1-t)+c1[i]*t) for i in range(3))
                od.line((max(0,cx1-r),y,min(W,cx2+r),y),fill=(*col,235))
            overlap_layer.putalpha(overlap)
            logo_layer.alpha_composite(overlap_layer)
            img.alpha_composite(logo_layer)

'''
text = text[:img_line_end] + logo_block + text[icons_start:]

# Remove somente o conteúdo textual do título. A label principal vira uma
# label vazia com a mesma fonte, preservando altura e posição dos campos.
lines = text.splitlines(keepends=True)
out = []
headline_replaced = False
for line in lines:
    if ('seu Login' in line and 'tk.Label' in line):
        indent = line[:len(line)-len(line.lstrip())]
        out.append(indent + "tk.Label(title, text=' ', font=('Segoe UI', 27, 'bold'), bg=RIGHT_BG, fg=RIGHT_BG).pack(side='left')\n")
        headline_replaced = True
        continue
    if ('tk.Label' in line and 'title' in line and "text='.'" in line):
        continue
    out.append(line)

if not headline_replaced:
    raise RuntimeError('Linha do titulo do login nao encontrada')
text = ''.join(out)

app.write_text(text, encoding='utf-8')
print('v44 login patch applied: interlocked CC + login title removed')
