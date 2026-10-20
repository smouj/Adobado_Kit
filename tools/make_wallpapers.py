import os, json, math, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "brand" / "wallpapers"
THEME = BASE / "installer" / "theme"
OUT.mkdir(parents=True, exist_ok=True)
THEME.mkdir(parents=True, exist_ok=True)
FONT = r"C:\Windows\Fonts\segoeuib.ttf" if Path(r"C:\Windows\Fonts\segoeuib.ttf").is_file() else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = r"C:\Windows\Fonts\segoeui.ttf" if Path(r"C:\Windows\Fonts\segoeui.ttf").is_file() else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
INK = (8,10,14)
CREAM = (238,242,246)
LIME = (184,243,74)
CORAL = (255,92,92)
BLUE = (91,141,239)
APPS = [("photo","PhotoAdobado",(255,92,92)),("art","ArtAdobado",(232,90,200)),("film","FilmAdobado",(255,159,67)),("effect","EffectAdobado",(155,123,255)),("light","LightAdobado",(242,201,76)),("sound","SoundAdobado",(53,200,216)),("design","DesignAdobado",(123,217,87)),("pdf","PdfAdobado",(79,131,232))]
SIZES = [
 (3840,2160,"desktop-4k","16:9","desktop"),
 (2560,1440,"desktop-qhd","16:9","desktop"),
 (1920,1080,"desktop-fhd","16:9","desktop"),
 (3440,1440,"ultrawide-21-9","21:9","ultrawide"),
 (2560,1600,"laptop-16-10","16:10","laptop"),
 (2048,1536,"tablet-4-3","4:3","tablet"),
 (1366,768,"laptop-hd","16:9","laptop"),
 (1170,2532,"phone-19-5-9","19.5:9","phone"),
 (1080,2400,"phone-20-9","20:9","phone"),
 (1440,2560,"phone-16-9","16:9","phone"),
 (2732,2048,"tablet-ipad","4:3","tablet"),
]

def base(w,h,seed=7):
    """Build a soft, deterministic brand background without external arrays."""
    image=Image.new("RGBA",(w,h),INK+(255,))
    scale=min(w,h)
    glows=[
      (0.16,0.20,0.32,0.40,CORAL),
      (0.84,0.16,0.36,0.35,BLUE),
      (0.62,0.86,0.40,0.25,(123,217,87)),
      (0.30,0.78,0.30,0.18,(155,123,255)),
    ]
    for cx,cy,radius,strength,color in glows:
        layer=Image.new("RGBA",(w,h),(0,0,0,0))
        draw=ImageDraw.Draw(layer)
        r=radius*scale
        x=cx*w; y=cy*h
        draw.ellipse((x-r,y-r,x+r,y+r),fill=tuple(color)+(round(255*strength),))
        layer=layer.filter(ImageFilter.GaussianBlur(max(1,int(scale*radius*0.52))))
        image=Image.alpha_composite(image,layer)
    # A restrained vignette gives the centered launcher mark enough contrast.
    radial=Image.radial_gradient("L").resize((w,h),Image.Resampling.BICUBIC)
    edge=Image.eval(radial,lambda value: 255-value)
    edge=edge.point(lambda value: round(value*0.32))
    shade=Image.new("RGBA",(w,h),(0,0,0,0))
    shade.putalpha(edge)
    return Image.alpha_composite(image,shade).convert("RGB")


def mark_layer(size, cx, cy, r):
    """Place the official launcher icon so wallpapers and app chrome agree."""
    layer=Image.new("RGBA",size,(0,0,0,0))
    glow=Image.new("RGBA",size,(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    gd.ellipse((cx-r*1.15,cy-r*1.15,cx+r*1.15,cy+r*1.15),fill=(184,243,74,34))
    layer=Image.alpha_composite(layer,glow.filter(ImageFilter.GaussianBlur(r*0.32)))
    icon_path=BASE/"launcher"/"launcher.png"
    if not icon_path.is_file():
        raise FileNotFoundError(f"Missing canonical launcher icon: {icon_path}")
    with Image.open(icon_path) as source:
        icon=source.convert("RGBA").resize((max(1,int(r*2)),max(1,int(r*2))),Image.Resampling.LANCZOS)
    layer.alpha_composite(icon,(int(cx-icon.width/2),int(cy-icon.height/2)))
    return layer


def text_layer(size, cx, y, fs, sub=None):
    layer=Image.new("RGBA",size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    try: f=ImageFont.truetype(FONT,fs)
    except: f=ImageFont.load_default()
    left="Adobado "; right="Kit"
    tw=d.textlength(left,font=f)+d.textlength(right,font=f)
    x=cx-tw/2
    d.text((x,y),left,font=f,fill=CREAM+(255,),anchor="ls")
    x2=x+d.textlength(left,font=f)
    d.text((x2,y),right,font=f,fill=LIME+(255,),anchor="ls")
    if sub:
        try: fr=ImageFont.truetype(FONT_R,int(fs*0.34))
        except: fr=ImageFont.load_default()
        d.text((cx,y+fs*0.66),sub,font=fr,fill=(152,163,177,255),anchor="ms")
    return layer

def text_left(size, x, y, fs):
    layer=Image.new("RGBA",size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    try: f=ImageFont.truetype(FONT,fs)
    except: f=ImageFont.load_default()
    d.text((x,y),"Adobado ",font=f,fill=CREAM+(255,),anchor="ls")
    x2=x+d.textlength("Adobado ",font=f)
    d.text((x2,y),"Kit",font=f,fill=LIME+(255,),anchor="ls")
    return layer

def compose(w,h,variant):
    img=base(w,h).convert("RGBA")
    m=min(w,h)
    if variant in ("prism","mobile"):
        cx,cy=w*0.5,h*0.44
        r=m*0.16
        img=Image.alpha_composite(img,mark_layer((w,h),cx,cy,r))
        img=Image.alpha_composite(img,text_layer((w,h),cx,cy+r*1.35,m*0.065,"Herramientas para tu próximo proyecto"))
        if variant=="mobile":
            # color bars bottom
            layer=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(layer)
            bw=w*0.09; gap=w*0.025; total=8*bw+7*gap; x=(w-total)/2; y=h*0.86
            for i,(slug,name,col) in enumerate(APPS):
                d.rounded_rectangle((x+i*(bw+gap),y,x+i*(bw+gap)+bw,y+h*0.012),radius=bw*0.3,fill=col+(255,))
            img=Image.alpha_composite(img,layer)
    elif variant=="orbit":
        cx,cy=w*0.5,h*0.42
        ring=m*0.26
        icons=[]
        for i,(slug,name,col) in enumerate(APPS):
            a=2*math.pi*i/8 - math.pi/2
            icons.append((cx+math.cos(a)*ring,cy+math.sin(a)*ring,slug,col))
        layer=Image.new("RGBA",(w,h),(0,0,0,0))
        for x,y,slug,col in icons:
            p=str(BASE/"assets"/"icons"/(slug+".png"))
            if os.path.isfile(p):
                ic=Image.open(p).convert("RGBA").resize((int(m*0.062),int(m*0.062)),Image.LANCZOS)
                layer.alpha_composite(ic,(int(x-ic.width/2),int(y-ic.height/2)))
        img=Image.alpha_composite(img,layer)
        img=Image.alpha_composite(img,mark_layer((w,h),cx,cy,m*0.07))
        img=Image.alpha_composite(img,text_layer((w,h),cx,h*0.88,m*0.055,"Ocho apps para proyectos distintos"))
    else:  # grid
        layer=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(layer)
        step=max(48,int(m*0.055))
        for gx in range(0,w,step): d.line((gx,0,gx,h),fill=(255,255,255,9),width=1)
        for gy in range(0,h,step): d.line((0,gy,w,gy),fill=(255,255,255,9),width=1)
        img=Image.alpha_composite(img,layer)
        r=m*0.055; cx=w*0.09; cy=h*0.80
        img=Image.alpha_composite(img,mark_layer((w,h),cx,cy,r))
        img=Image.alpha_composite(img,text_left((w,h),cx+r*1.55,cy+r*0.18,m*0.045))
    return img.convert("RGB")

manifest={"brand":"Adobado Kit","version":"1.0","variants":["prism","orbit","grid"],"wallpapers":[]}
for w,h,slug,aspect,device in SIZES:
    for variant in ("prism","orbit","grid"):
        img=compose(w,h,variant)
        name="adobado-%s-%s.jpg" % (variant,slug)
        img.save(str(OUT/name),quality=92,optimize=True)
        manifest["wallpapers"].append({"file":name,"variant":variant,"width":w,"height":h,"aspect":aspect,"devices":[device]})
# contact sheet 4 variants at 1280x720
sheet=Image.new("RGB",(2*640+30,2*360+30),(8,10,14))
for i,variant in enumerate(("prism","orbit","grid")):
    im=compose(1280,720,variant).resize((640,360),Image.LANCZOS)
    x=10+(i%2)*(640+10); y=10+(i//2)*(360+10)
    sheet.paste(im,(x,y))
sheet.save(str(OUT/"preview.jpg"),quality=92)
json.dump(manifest,open(OUT/"manifest.json","w",encoding="utf-8"),indent=2)

# installer theme
wi=compose(164,314,"prism")
wi.save(str(THEME/"wizard.bmp"))
sm=Image.new("RGB",(55,55),(11,14,19))
icon=Image.open(str(BASE/"launcher"/"launcher.png")).convert("RGBA").resize((44,44),Image.LANCZOS)
sm.paste(icon,(5,5),icon)
sm.save(str(THEME/"wizard-small.bmp"))
shutil.copy2(str(BASE/"launcher"/"launcher.ico"),str(THEME/"setup.ico"))
shutil.copy2(str(BASE/"launcher"/"launcher.ico"),str(THEME/"uninstall.ico"))
compose(1920,1080,"prism").save(str(THEME/"installer-bg.jpg"),quality=92)
print("wallpapers/theme ok", len(manifest["wallpapers"]))
