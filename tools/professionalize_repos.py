import os, io, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ICONS = "/home/smouj/.openclaw/workspace/infest/apps/adobado-kit/assets/icons"
INK=(11,14,19); CREAM=(238,242,246); MUTED=(152,163,177); LIME=(184,243,74)

APPS = [
 ("PhotoAdobado","/home/smouj/PhotoAdobado-standalone","photo",(255,92,92),"Probada en Windows",True),
 ("ArtAdobado","/home/smouj/adobado-import/ArtAdobado","art",(232,90,200),"Build OK · artifact pendiente",False),
 ("FilmAdobado","/home/smouj/adobado-import/FilmAdobado","film",(255,159,67),"Probada en Windows",True),
 ("EffectAdobado","/home/smouj/adobado-import/EffectAdobado","effect",(155,123,255),"Build OK · artifact pendiente",False),
 ("LightAdobado","/home/smouj/adobado-import/LightAdobado","light",(255,224,102),"Build OK · artifact pendiente",False),
 ("SoundAdobado","/home/smouj/adobado-import/SoundAdobado","sound",(77,214,232),"Probada en Windows",True),
 ("DesignAdobado","/home/smouj/adobado-import/DesignAdobado","design",(139,224,78),"Build OK · artifact pendiente",False),
 ("PdfAdobado","/home/smouj/adobado-import/PdfAdobado","pdf",(91,141,239),"Repo creado · build en curso",False),
]

def preview(app, dest, slug, hue, status):
    W,H=1200,675
    img=Image.new("RGB",(W,H),INK); d=ImageDraw.Draw(img)
    # glows
    for cx,cy,rad,col in [(180,120,420,(hue[0],hue[1],hue[2])),(1050,600,460,(91,141,239)),(700,80,360,(184,243,74))]:
        layer=Image.new("RGBA",(W,H),(0,0,0,0)); ld=ImageDraw.Draw(layer)
        ld.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=col+(40,))
        layer=layer.filter(ImageFilter.GaussianBlur(90)); img=Image.alpha_composite(img.convert("RGBA"),layer).convert("RGB")
    d=ImageDraw.Draw(img)
    ic=Image.open(os.path.join(ICONS,slug+".png")).convert("RGBA").resize((210,210),Image.LANCZOS)
    img.paste(ic,(80,110),ic)
    try: f1=ImageFont.truetype(FONT,64); f2=ImageFont.truetype(FONT_R,30); f3=ImageFont.truetype(FONT,22); f4=ImageFont.truetype(FONT_R,20)
    except: f1=f2=f3=f4=ImageFont.load_default()
    d.text((330,140),app,font=f1,fill=CREAM)
    d.text((332,230),status,font=f2,fill=CREAM if "Probada" in status else MUTED)
    d.text((332,290),"Herramienta local de Adobado Kit",font=f2,fill=MUTED)
    d.rounded_rectangle((80,560,1120,562),radius=1,fill=(37,44,55))
    d.text((80,590),"Adobado Kit · vista previa de marca",font=f4,fill=MUTED)
    d.text((80,620),"Interfaz pendiente de build/probado en Windows",font=f4,fill=(120,132,147))
    os.makedirs(os.path.join(dest,"docs"),exist_ok=True)
    img.save(os.path.join(dest,"docs","preview.png"))

STAR='[![Stars](https://img.shields.io/github/stars/smouj/%s?style=flat&color=FF5C5C)](https://github.com/smouj/%s/stargazers)'
SEC='''# Security\n\nReporta vulnerabilidades de forma privada al mantenedor (SMOUJ013) antes de abrirlas en publico.\n\n- Las apps son locales; no hay backend ni telemetria.\n- No se aceptan dependencias que envien archivos a servidores.\n- No se publican binarios sin revisar licencias y procedencia.\n'''
COC='''# Codigo de conducta\n\nEspacio respetuoso y directo.\n\n- Critica tecnica, sin ataques personales.\n- Nada de discriminacion, acoso ni lenguaje hostil.\n- Respeta las licencias y el trabajo de terceros.\n- Los desacuerdos se resuelven con argumentos y pruebas.\n'''

for app,dest,slug,hue,status,has_shot in APPS:
    if not os.path.isdir(dest):
        print("MISSING",app); continue
    if not has_shot:
        preview(app,dest,slug,hue,status)
    p=os.path.join(dest,"README.md")
    if not os.path.isfile(p):
        print("NO README",app); continue
    t=io.open(p,encoding="utf-8").read()
    if "img.shields.io/github/stars" not in t:
        sb=STAR % (app,app)
        marker="[![Adobado Kit]"
        if marker in t:
            t=t.replace(marker,sb+"\n"+marker,1)
        else:
            lines=t.split(chr(10)); lines.insert(1,sb); t=chr(10).join(lines)
    if (not has_shot) and "docs/preview.png" not in t and os.path.isfile(os.path.join(dest,"docs","preview.png")):
        line="![%s](docs/preview.png)" % app
        lines=t.split(chr(10)); idx=None
        for i,l in enumerate(lines):
            if l.startswith("## Estado"): idx=i; break
        if idx is None:
            for i,l in enumerate(lines):
                if i>0 and l.startswith("## "): idx=i; break
        if idx is None: idx=len(lines)
        lines[idx:idx]=[line,""]; t=chr(10).join(lines)
    io.open(p,"w",encoding="utf-8").write(t)
    for name,content in (("SECURITY.md",SEC),("CODE_OF_CONDUCT.md",COC)):
        fp=os.path.join(dest,name)
        if not os.path.isfile(fp): io.open(fp,"w",encoding="utf-8").write(content)
    subprocess.run(["git","add","-A"],cwd=dest,check=True)
    st=subprocess.run(["git","status","--porcelain"],cwd=dest,capture_output=True,text=True).stdout.strip()
    if not st:
        print(app,"no changes"); continue
    subprocess.run(["git","-c","user.name=smouj","-c","user.email=hecpoley11@gmail.com","commit","-qm","Professionalize README badges, preview and policy docs"],cwd=dest,check=True)
    p2=subprocess.run(["git","push","-q","origin","main"],cwd=dest,capture_output=True,text=True)
    print(app,"push",p2.returncode)

# Kit README
kit="/home/smouj/.openclaw/workspace/infest/apps/adobado-kit"
p=os.path.join(kit,"README.md"); t=io.open(p,encoding="utf-8").read()
if '<img src="assets/logo.svg"' not in t:
    t=t.replace("# Adobado Kit\n\n",'# Adobado Kit\n\n<p align="center"><img src="assets/logo.svg" width="96" alt="Adobado Kit"></p>\n\n',1)
if "github/stars/smouj/Adobado_Kit" not in t:
    sb='[![Stars](https://img.shields.io/github/stars/smouj/Adobado_Kit?style=flat&color=B8F34A)](https://github.com/smouj/Adobado_Kit/stargazers)'
    marker="[![License: MIT]"
    if marker in t: t=t.replace(marker,sb+"\n"+marker,1)
for slug,app in [("photo","PhotoAdobado"),("art","ArtAdobado"),("film","FilmAdobado"),("effect","EffectAdobado"),("light","LightAdobado"),("sound","SoundAdobado"),("design","DesignAdobado"),("pdf","PdfAdobado")]:
    t=t.replace("| ["+app+"]",'| <img src="assets/icons/%s.png" width="22" alt=""> [%s]' % (slug,app),1)
io.open(p,"w",encoding="utf-8").write(t)
print("kit readme updated")
