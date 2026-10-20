import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/smouj/.openclaw/workspace/infest/apps/adobado-kit/assets/icons"
OSVG = os.path.join(OUT, "svg")
os.makedirs(OUT, exist_ok=True)
os.makedirs(OSVG, exist_ok=True)

S = 1024
INK = (11, 14, 19, 255)
CREAM = (238, 242, 246, 255)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

APPS = [
    ("photo",  "PhotoAdobado",  "#FF5C5C"),
    ("art",    "ArtAdobado",    "#E85AC8"),
    ("film",   "FilmAdobado",   "#FF9F43"),
    ("effect", "EffectAdobado", "#9B7BFF"),
    ("light",  "LightAdobado",  "#FFE066"),
    ("sound",  "SoundAdobado",  "#4DD6E8"),
    ("design", "DesignAdobado", "#8BE04E"),
    ("pdf",    "PdfAdobado",    "#5B8DEF"),
]

def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), 255)

def rline(d, p1, p2, color, width):
    d.line([p1, p2], fill=color, width=width)
    r = width // 2
    for p in (p1, p2):
        d.ellipse((p[0]-r, p[1]-r, p[0]+r, p[1]+r), fill=color)

def polyline(d, pts, color, width):
    for i in range(len(pts)-1):
        rline(d, pts[i], pts[i+1], color, width)

def glyph(d, slug, hue, ink=CREAM):
    hue = hx(hue)
    if slug == "photo":
        d.ellipse((302,302,722,722), outline=ink, width=44)
        pts=[]
        for i in range(6):
            a = math.radians(-90 + 60*i)
            pts.append((512+math.cos(a)*100, 512+math.sin(a)*100))
        polyline(d, pts+[pts[0]], ink, 34)
        for i in range(6):
            a = math.radians(-90 + 60*i)
            rline(d, (512+math.cos(a)*100,512+math.sin(a)*100), (512+math.cos(a)*210,512+math.sin(a)*210), ink, 32)
        d.ellipse((484,484,540,540), fill=hue)
    elif slug == "art":
        pts=[(512,270),(754,512),(512,754),(270,512)]
        polyline(d, pts+[pts[0]], ink, 44)
        for p in pts:
            d.ellipse((p[0]-26,p[1]-26,p[0]+26,p[1]+26), fill=ink)
        d.ellipse((472,472,552,552), fill=hue)
    elif slug == "film":
        d.ellipse((302,302,722,722), outline=ink, width=44)
        for p in [(512,378),(646,512),(512,646),(378,512)]:
            d.ellipse((p[0]-46,p[1]-46,p[0]+46,p[1]+46), fill=ink)
        d.ellipse((478,478,546,546), fill=hue)
    elif slug == "effect":
        pts=[]
        for i in range(8):
            a=math.radians(-90+45*i)
            r=230 if i%2==0 else 74
            pts.append((512+math.cos(a)*r,512+math.sin(a)*r))
        d.polygon(pts, fill=hue)
        d.ellipse((482,482,542,542), fill=ink)
    elif slug == "light":
        d.ellipse((400,400,624,624), outline=ink, width=44)
        for i in range(8):
            a=math.radians(45*i)
            rline(d, (512+math.cos(a)*166,512+math.sin(a)*166), (512+math.cos(a)*232,512+math.sin(a)*232), hue, 44)
        d.ellipse((480,480,544,544), fill=hue)
    elif slug == "sound":
        heights=[180,300,420,300,180]
        xs=[312,412,512,612,712]
        for i,(x,h) in enumerate(zip(xs,heights)):
            col = hue if i==2 else ink
            d.rounded_rectangle((x,512-h//2,x+52,512+h//2), radius=26, fill=col)
    elif slug == "design":
        for (x,y) in [(302,302),(542,302),(302,542),(542,542)]:
            d.rounded_rectangle((x,y,x+180,y+180), radius=32, outline=ink, width=40)
        d.rounded_rectangle((542,302,722,482), radius=32, fill=hue)
    elif slug == "pdf":
        d.rounded_rectangle((330,240,694,784), radius=40, outline=ink, width=44)
        for y in (380,470,560):
            rline(d, (400,y), (624,y), ink, 26)
        try:
            font=ImageFont.truetype(FONT,120)
        except Exception:
            font=ImageFont.load_default()
        d.text((512,690), "PDF", font=font, fill=hue, anchor="mm")

def svg_glyph(slug, hue):
    h = hue
    if slug == "photo":
        pts=[]
        for i in range(6):
            a=math.radians(-90+60*i)
            pts.append("%.1f,%.1f" % (512+math.cos(a)*100, 512+math.sin(a)*100))
        lines=[]
        for i in range(6):
            a=math.radians(-90+60*i)
            lines.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (512+math.cos(a)*100,512+math.sin(a)*100,512+math.cos(a)*210,512+math.sin(a)*210))
        return '<circle cx="512" cy="512" r="210" fill="none" stroke="#EEF2F6" stroke-width="44"/><polygon points="%s" fill="none" stroke="#EEF2F6" stroke-width="34" stroke-linejoin="round"/>%s<circle cx="512" cy="512" r="28" fill="%s"/>' % (" ".join(pts), "".join(lines), h)
    if slug == "art":
        return '<polygon points="512,270 754,512 512,754 270,512" fill="none" stroke="#EEF2F6" stroke-width="44" stroke-linejoin="round"/><circle cx="512" cy="270" r="26" fill="#EEF2F6"/><circle cx="754" cy="512" r="26" fill="#EEF2F6"/><circle cx="512" cy="754" r="26" fill="#EEF2F6"/><circle cx="270" cy="512" r="26" fill="#EEF2F6"/><circle cx="512" cy="512" r="40" fill="%s"/>' % h
    if slug == "film":
        return '<circle cx="512" cy="512" r="210" fill="none" stroke="#EEF2F6" stroke-width="44"/><circle cx="512" cy="378" r="46" fill="#EEF2F6"/><circle cx="646" cy="512" r="46" fill="#EEF2F6"/><circle cx="512" cy="646" r="46" fill="#EEF2F6"/><circle cx="378" cy="512" r="46" fill="#EEF2F6"/><circle cx="512" cy="512" r="34" fill="%s"/>' % h
    if slug == "effect":
        pts=[]
        for i in range(8):
            a=math.radians(-90+45*i); r=230 if i%2==0 else 74
            pts.append("%.1f,%.1f" % (512+math.cos(a)*r,512+math.sin(a)*r))
        return '<polygon points="%s" fill="%s"/><circle cx="512" cy="512" r="30" fill="#EEF2F6"/>' % (" ".join(pts), h)
    if slug == "light":
        rays=[]
        for i in range(8):
            a=math.radians(45*i)
            rays.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="44" stroke-linecap="round"/>' % (512+math.cos(a)*166,512+math.sin(a)*166,512+math.cos(a)*232,512+math.sin(a)*232,h))
        return '<circle cx="512" cy="512" r="112" fill="none" stroke="#EEF2F6" stroke-width="44"/>%s<circle cx="512" cy="512" r="32" fill="%s"/>' % ("".join(rays), h)
    if slug == "sound":
        bars=[]
        for x,hgt in [(312,180),(412,300),(512,420),(612,300),(712,180)]:
            col = h if x==512 else "#EEF2F6"
            bars.append('<rect x="%d" y="%d" width="52" height="%d" rx="26" fill="%s"/>' % (x,512-hgt//2,hgt,col))
        return "".join(bars)
    if slug == "design":
        return '<rect x="302" y="302" width="180" height="180" rx="32" fill="none" stroke="#EEF2F6" stroke-width="40"/><rect x="542" y="302" width="180" height="180" rx="32" fill="%s"/><rect x="302" y="542" width="180" height="180" rx="32" fill="none" stroke="#EEF2F6" stroke-width="40"/><rect x="542" y="542" width="180" height="180" rx="32" fill="none" stroke="#EEF2F6" stroke-width="40"/>' % h
    if slug == "pdf":
        return '<rect x="330" y="240" width="364" height="544" rx="40" fill="none" stroke="#EEF2F6" stroke-width="44"/><line x1="400" y1="380" x2="624" y2="380" stroke="#EEF2F6" stroke-width="26" stroke-linecap="round"/><line x1="400" y1="470" x2="624" y2="470" stroke="#EEF2F6" stroke-width="26" stroke-linecap="round"/><line x1="400" y1="560" x2="624" y2="560" stroke="#EEF2F6" stroke-width="26" stroke-linecap="round"/><text x="512" y="730" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-weight="700" font-size="120" fill="%s">PDF</text>' % h

def tile(d, hue):
    d.rounded_rectangle((32,32,S-32,S-32), radius=220, fill=INK, outline=hx(hue), width=36)
    d.rounded_rectangle((92,92,S-92,S-92), radius=176, outline=(255,255,255,22), width=3)

def svg(slug, hue):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">'
            '<rect x="32" y="32" width="960" height="960" rx="220" fill="#0B0E13" stroke="%s" stroke-width="36"/>'
            '<rect x="92" y="92" width="840" height="840" rx="176" fill="none" stroke="#FFFFFF" stroke-opacity="0.09" stroke-width="3"/>'
            '%s</svg>') % (hue, svg_glyph(slug, hue))

thumbs=[]
for slug, name, hue in APPS:
    img=Image.new("RGBA",(S,S),(0,0,0,0)); d=ImageDraw.Draw(img)
    tile(d,hue); glyph(d,slug,hue)
    img.save(os.path.join(OUT, slug+".png"))
    img.save(os.path.join(OUT, slug+".ico"), sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
    open(os.path.join(OSVG, slug+".svg"),"w",encoding="utf-8").write(svg(slug,hue))
    thumbs.append((slug,img.resize((256,256),Image.LANCZOS)))

sheet=Image.new("RGB",(4*300+40,2*340+40),(8,10,14)); sd=ImageDraw.Draw(sheet)
for i,(slug,img) in enumerate(thumbs):
    x=40+(i%4)*300; y=40+(i//4)*340
    sheet.paste(img,(x,y),img)
    sd.text((x,y+270),slug.capitalize()+"Adobado",fill=(238,242,246))
sheet.save(os.path.join(OUT,"family.png"))
print("icons v2 ok")
