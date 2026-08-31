from pathlib import Path
from PIL import Image, ImageDraw
import PIL.ImageChops as IC

# Logo/icone CC transparente
data = Path('data')
data.mkdir(exist_ok=True)
S = 1024
scale = 4
hi = Image.new('RGBA', (S*scale, S*scale), (0, 0, 0, 0))
d = ImageDraw.Draw(hi)
cx1, cx2, cy = 360*scale, 650*scale, 510*scale
r, stroke = 285*scale, 122*scale
box1 = (cx1-r, cy-r, cx1+r, cy+r)
box2 = (cx2-r, cy-r, cx2+r, cy+r)
start, end = 42, 318

def lerp(a, b, t):
    return tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))

steps = 420
for i in range(steps):
    t = i/(steps-1)
    a0 = start + (end-start)*i/steps
    a1 = start + (end-start)*(i+1)/steps + 0.35
    left = lerp((11, 108, 126), (30, 145, 157), t)
    right = lerp((61, 173, 173), (88, 197, 190), t)
    d.arc(box1, a0, a1, fill=left+(255,), width=stroke)
    d.arc(box2, a0, a1, fill=right+(255,), width=stroke)

mask1 = Image.new('L', hi.size, 0)
mask2 = Image.new('L', hi.size, 0)
ImageDraw.Draw(mask1).arc(box1, start, end, fill=255, width=stroke)
ImageDraw.Draw(mask2).arc(box2, start, end, fill=255, width=stroke)
overlap = IC.multiply(mask1, mask2)
dark = Image.new('RGBA', hi.size, (41, 59, 72, 218))
hi.alpha_composite(Image.composite(dark, Image.new('RGBA', hi.size, (0,0,0,0)), overlap))

img = hi.resize((S, S), Image.Resampling.LANCZOS)
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)
pad = 60
side = max(img.width, img.height)+pad*2
square = Image.new('RGBA', (side, side), (0,0,0,0))
square.alpha_composite(img, ((side-img.width)//2, (side-img.height)//2))
square.save(data/'cc_logo.png')
square.save(data/'cc_logo.ico', sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)])

# Ajustes da tela de login
app = Path('src/controle_contas/app.py')
text = app.read_text(encoding='utf-8')

# Icone da janela
marker = "super().__init__(); self.title('Controle de Contas');self.geometry('1440x860');self.minsize(1180,720);self.configure(bg=BG)"
if marker in text and "cc_logo.ico" not in text:
    replacement = marker + "\n        try:\n            ico = resource('data/cc_logo.ico')\n            png = resource('data/cc_logo.png')\n            if ico.exists(): self.iconbitmap(default=str(ico))\n            if png.exists():\n                self._window_icon = tk.PhotoImage(file=str(png))\n                self.iconphoto(True, self._window_icon)\n        except Exception:\n            pass"
    text = text.replace(marker, replacement, 1)

# Fundo solido, sem gradientes/faixas de tons
start_marker = "            img=Image.new('RGBA',(W,H),(6,11,20,255))\n            d=ImageDraw.Draw(img)\n"
end_marker = "            paste_cc_logo(img, W, H)\n"
if start_marker in text and end_marker in text:
    a = text.index(start_marker)
    b = text.index(end_marker, a)
    text = text[:a] + "            img=Image.new('RGBA',(W,H),(5,10,18,255))\n\n" + text[b:]

# Mais icones discretos espalhados
old_icons = """            doc_icon(W*0.08,H*0.18,32*scale,18)\n            doc_icon(W*0.50,H*0.23,26*scale,14)\n            doc_icon(W*0.56,H*0.74,22*scale,12)\n"""
new_icons = """            doc_icon(W*0.08,H*0.17,30*scale,16)\n            doc_icon(W*0.18,H*0.42,22*scale,10)\n            doc_icon(W*0.30,H*0.70,20*scale,9)\n            doc_icon(W*0.50,H*0.23,24*scale,12)\n            doc_icon(W*0.60,H*0.52,18*scale,9)\n            doc_icon(W*0.56,H*0.74,20*scale,10)\n            doc_icon(W*0.82,H*0.22,22*scale,10)\n            doc_icon(W*0.86,H*0.70,18*scale,8)\n"""
if old_icons in text:
    text = text.replace(old_icons, new_icons, 1)

app.write_text(text, encoding='utf-8')
print('v41 patch applied')
