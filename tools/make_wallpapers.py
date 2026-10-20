import os, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/home/smouj/.openclaw/workspace/infest/apps/adobado-kit"
OUT = os.path.join(BASE, "brand", "wallpapers")
THEME = os.path.join(BASE, "installer", "theme")
os.makedirs(OUT, exist_ok=True)
os.makedirs(THEME, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
INK = (8,10,14)
CREAM = (238,242,246)
LIME = (184,243,74)
CORAL = (255,92,92)
BLUE = (91,141,239)
APPS = [("photo","PhotoAdobado",CORAL),("art","ArtAdobado",(232,90,200)),("film","FilmAdobado",(255,159,67)),("effect","EffectAdobado",(155,123,255)),("light","LightAdobado",(255,224,102)),("sound","SoundAdobado",(77,214,232)),("design","DesignAdobado",(139,224,78)),("pdf","PdfAdobado",(91,141,239))]
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
    rng=np.random.default_rng(seed)
    y,x=np.mgrid[0:h,0:w].astype(np.float32)
    arr=np.zeros((h,w,3),dtype=np.float32)
    arr[:]=np.array(INK,dtype=np.float32)
    glows=[
      (0.16,0.20,0.32,0.40,CORAL),
      (0.84,0.16,0.36,0.35,BLUE),
      (0.62,0.86,0.40,0.25,(139,224,78)),
      (0.30,0.78,0.30,0.18,(155,123,255)),
    ]
    for cx,cy,sig,strength,col in glows:
        d2=((x-cx*w)**2+(y-cy*h)**2)/(2*(sig*min(w,h))**2)
        g=np.exp(-d2).astype(np.float32)*strength
        for i in range(3):
            arr[:,:,i]+=g*col[i]
    # vignette
    nx=(x/w-0.5)*2; ny=(y/h-0.5)*2
    v=np.clip(1-0.38*(nx*nx+ny*ny),0.35,1).astype(np.float32)
    arr*=v[:,:,None]
    arr+=rng.normal(0,1.6,(h,w,1)).astype(np.float32)
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8),"RGB")

def mark_layer(size, cx, cy, r):
    layer=Image.new("RGBA",(size[0],size[1]),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    # glow
    glow=Image.new("RGBA",(size[0],size[1]),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    gd.ellipse((cx-r*0.9,cy-r*0.9,cx+r*0.9,cy+r*0.9),fill=(184,243,74,40))
    glow=glow.filter(ImageFilter.GaussianBlur(r*0.35))
    layer=Image.alpha_composite(layer,glow)
    d=ImageDraw.Draw(layer)
    cr=r*0.34
    d.ellipse((cx-r*0.30-cr,cy-r*0.12-cr,cx-r*0.30+cr,cy-r*0.12+cr),fill=CORAL+(255,))
    d.ellipse((cx+r*0.30-cr,cy-r*0.12-cr,cx+r*0.30+cr,cy-r*0.12+cr),fill=BLUE+(255,))
    d.rounded_rectangle((cx-r*0.46,cy+r*0.26,cx+r*0.46,cy+r*0.44),radius=r*0.09,fill=LIME+(255,))
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
        img=Image.alpha_composite(img,text_layer((w,h),cx,cy+r*1.35,m*0.065,"Herramientas creativas locales"))
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
            p=os.path.join(BASE,"assets","icons",slug+".png")
            if os.path.isfile(p):
                ic=Image.open(p).convert("RGBA").resize((int(m*0.062),int(m*0.062)),Image.LANCZOS)
                layer.alpha_composite(ic,(int(x-ic.width/2),int(y-ic.height/2)))
        img=Image.alpha_composite(img,layer)
        img=Image.alpha_composite(img,mark_layer((w,h),cx,cy,m*0.07))
        img=Image.alpha_composite(img,text_layer((w,h),cx,h*0.88,m*0.055,"Ocho herramientas. Un kit."))
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
        img.save(os.path.join(OUT,name),quality=92,optimize=True)
        manifest["wallpapers"].append({"file":name,"variant":variant,"width":w,"height":h,"aspect":aspect,"devices":[device]})
# contact sheet 4 variants at 1280x720
sheet=Image.new("RGB",(2*640+30,2*360+30),(8,10,14))
for i,variant in enumerate(("prism","orbit","grid")):
    im=compose(1280,720,variant).resize((640,360),Image.LANCZOS)
    x=10+(i%2)*(640+10); y=10+(i//2)*(360+10)
    sheet.paste(im,(x,y))
sheet.save(os.path.join(OUT,"preview.jpg"),quality=92)
json.dump(manifest,open(os.path.join(OUT,"manifest.json"),"w",encoding="utf-8"),indent=2)

# installer theme
wi=compose(164,314,"prism")
wi.save(os.path.join(THEME,"wizard.bmp"))
sm=Image.new("RGB",(55,55),(11,14,19))
icon=Image.open(os.path.join(BASE,"launcher","icons","launcher.ico")).convert("RGBA").resize((44,44),Image.LANCZOS)
sm.paste(icon,(5,5),icon)
sm.save(os.path.join(THEME,"wizard-small.bmp"))
import shutil
shutil.copy2(os.path.join(BASE,"launcher","launcher.ico"),os.path.join(THEME,"setup.ico"))
shutil.copy2(os.path.join(BASE,"launcher","launcher.ico"),os.path.join(THEME,"uninstall.ico"))
compose(1920,1080,"prism").save(os.path.join(THEME,"installer-bg.jpg"),quality=92)
print("wallpapers/theme ok", len(manifest["wallpapers"]))
