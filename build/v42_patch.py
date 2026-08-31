from pathlib import Path

app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# Uma unica cor em toda a area de fundo da tela de login.
SOLID = '#050a12'
for old in ("        NAVY = '#060b14'", "        NAVY = '#05080f'", "        NAVY = '#050a12'"):
    text = text.replace(old, f"        NAVY = '{SOLID}'")
for old in ("        RIGHT_BG = '#05080f'", "        RIGHT_BG = '#060b14'", "        RIGHT_BG = '#050a12'"):
    text = text.replace(old, f"        RIGHT_BG = '{SOLID}'")

# Preserva exatamente o logo aprovado da versao anterior, priorizando a funcao
# que cola o asset transparente sem halo. O fallback tambem usa o asset PNG.
if 'def paste_cc_logo' in text:
    logo_code = "            paste_cc_logo(img, W, H)\n"
else:
    logo_code = """            try:\n                logo_path=resource('data/cc_logo.png')\n                logo=Image.open(logo_path).convert('RGBA')\n                target=int(min(W,H)*0.40)\n                logo.thumbnail((target,target), Image.Resampling.LANCZOS)\n                lx=int(W*0.29-logo.width/2); ly=int(H*0.42-logo.height/2)\n                img.alpha_composite(logo,(lx,ly))\n            except Exception:\n                pass\n"""

start = text.find('        def render_background(w, h):\n')
end = text.find('        def redraw():\n', start)
if start < 0 or end < 0:
    raise RuntimeError('Bloco render_background nao encontrado')

new_block = '''        def render_background(w, h):
            scale=2
            W=max(1100,int(w))*scale; H=max(650,int(h))*scale
            # Fundo 100% solido: sem degrade, faixas, brilho ou ondas.
            img=Image.new('RGBA',(W,H),(5,10,18,255))

''' + logo_code + '''
            icons=Image.new('RGBA',(W,H),(0,0,0,0))
            idraw=ImageDraw.Draw(icons)
            base=(68,92,146)

            def col(alpha):
                return (*base, int(alpha))

            def receipt_icon(x,y,sz,alpha=14):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.2*scale))
                c=col(alpha); w=int(sz*0.78); h=int(sz*1.10)
                pts=[(x,y),(x+w,y),(x+w,y+h-int(sz*.12)),(x+w-int(sz*.09),y+h),(x+w-int(sz*.18),y+h-int(sz*.08)),(x+w-int(sz*.27),y+h),(x+w-int(sz*.36),y+h-int(sz*.08)),(x+w-int(sz*.45),y+h),(x,y+h-int(sz*.12)),(x,y)]
                idraw.line(pts, fill=c, width=lw, joint='curve')
                for k, frac in enumerate((.30,.48,.66)):
                    yy=y+int(h*frac)
                    idraw.line((x+int(w*.18),yy,x+int(w*(.74 if k<2 else .56)),yy), fill=c, width=lw)

            def calendar_icon(x,y,sz,alpha=12):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.2*scale)); c=col(alpha)
                w=int(sz*1.0); h=int(sz*.88); r=max(3,int(sz*.12))
                idraw.rounded_rectangle((x,y+int(sz*.12),x+w,y+h), radius=r, outline=c, width=lw)
                idraw.line((x,y+int(sz*.33),x+w,y+int(sz*.33)), fill=c, width=lw)
                for dx in (.25,.72):
                    xx=x+int(w*dx); idraw.line((xx,y,xx,y+int(sz*.22)), fill=c, width=lw)
                for row in range(2):
                    for column in range(3):
                        cx=x+int(w*(.22+.27*column)); cy=y+int(sz*(.48+.20*row)); rr=max(1,int(sz*.035))
                        idraw.ellipse((cx-rr,cy-rr,cx+rr,cy+rr), fill=c)

            def calculator_icon(x,y,sz,alpha=12):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.15*scale)); c=col(alpha)
                w=int(sz*.76); h=int(sz*1.08); r=max(3,int(sz*.11))
                idraw.rounded_rectangle((x,y,x+w,y+h), radius=r, outline=c, width=lw)
                idraw.rounded_rectangle((x+int(w*.16),y+int(h*.12),x+int(w*.84),y+int(h*.31)), radius=max(2,int(r*.45)), outline=c, width=lw)
                for row in range(2):
                    for column in range(3):
                        bx=x+int(w*(.22+.27*column)); by=y+int(h*(.50+.23*row)); rr=max(1,int(sz*.045))
                        idraw.rounded_rectangle((bx-rr*2,by-rr*2,bx+rr*2,by+rr*2), radius=rr, outline=c, width=max(1,lw-1))

            def card_icon(x,y,sz,alpha=11):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.15*scale)); c=col(alpha)
                w=int(sz*1.25); h=int(sz*.76); r=max(3,int(sz*.11))
                idraw.rounded_rectangle((x,y,x+w,y+h), radius=r, outline=c, width=lw)
                idraw.line((x,y+int(h*.32),x+w,y+int(h*.32)), fill=c, width=lw)
                idraw.rounded_rectangle((x+int(w*.12),y+int(h*.58),x+int(w*.34),y+int(h*.70)), radius=max(1,int(r*.35)), outline=c, width=max(1,lw-1))

            def check_icon(x,y,sz,alpha=11):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.25*scale)); c=col(alpha)
                r=int(sz*.43); cx=x+r; cy=y+r
                idraw.ellipse((cx-r,cy-r,cx+r,cy+r), outline=c, width=lw)
                idraw.line((cx-int(r*.48),cy,cx-int(r*.10),cy+int(r*.34),cx+int(r*.56),cy-int(r*.42)), fill=c, width=lw, joint='curve')

            def wallet_icon(x,y,sz,alpha=10):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.15*scale)); c=col(alpha)
                w=int(sz*1.15); h=int(sz*.80); r=max(3,int(sz*.10))
                idraw.rounded_rectangle((x,y,x+w,y+h), radius=r, outline=c, width=lw)
                flap=(x+int(w*.60),y+int(h*.28),x+w+int(sz*.10),y+int(h*.64))
                idraw.rounded_rectangle(flap, radius=max(2,int(r*.60)), outline=c, width=lw)
                cx=x+int(w*.79); cy=y+int(h*.46); rr=max(1,int(sz*.035))
                idraw.ellipse((cx-rr,cy-rr,cx+rr,cy+rr), fill=c)

            def lightning_icon(x,y,sz,alpha=10):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.20*scale)); c=col(alpha)
                pts=[(x+int(sz*.56),y),(x+int(sz*.18),y+int(sz*.55)),(x+int(sz*.47),y+int(sz*.55)),(x+int(sz*.28),y+sz),(x+int(sz*.82),y+int(sz*.36)),(x+int(sz*.52),y+int(sz*.36)),(x+int(sz*.56),y)]
                idraw.line(pts, fill=c, width=lw, joint='curve')

            def drop_icon(x,y,sz,alpha=9):
                x=int(x); y=int(y); sz=int(sz); lw=max(2,int(1.15*scale)); c=col(alpha)
                pts=[(x+int(sz*.50),y),(x+int(sz*.20),y+int(sz*.44)),(x+int(sz*.16),y+int(sz*.62)),(x+int(sz*.24),y+int(sz*.82)),(x+int(sz*.50),y+sz),(x+int(sz*.76),y+int(sz*.82)),(x+int(sz*.84),y+int(sz*.62)),(x+int(sz*.80),y+int(sz*.44)),(x+int(sz*.50),y)]
                idraw.line(pts, fill=c, width=lw, joint='curve')

            receipt_icon(W*.075,H*.15,31*scale,15)
            calendar_icon(W*.18,H*.42,25*scale,10)
            calculator_icon(W*.30,H*.69,24*scale,9)
            card_icon(W*.49,H*.21,25*scale,11)
            check_icon(W*.57,H*.56,22*scale,9)
            receipt_icon(W*.55,H*.77,20*scale,8)
            wallet_icon(W*.82,H*.17,23*scale,9)
            drop_icon(W*.90,H*.47,21*scale,8)
            lightning_icon(W*.79,H*.72,23*scale,8)

            img=Image.alpha_composite(img, icons)
            return ImageTk.PhotoImage(img.resize((max(1100,int(w)), max(650,int(h))), Image.Resampling.LANCZOS))

'''

text = text[:start] + new_block + text[end:]
app.write_text(text, encoding='utf-8')
print('v42 patch applied: solid background + diversified account-control icons')
