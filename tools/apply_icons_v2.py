import os, io, re, shutil, subprocess, importlib.util
from PIL import Image, ImageDraw

BASE = "/home/smouj/.openclaw/workspace/infest/apps/adobado-kit"
ICONS = os.path.join(BASE, "assets", "icons")
spec = importlib.util.spec_from_file_location("iconsv2", os.path.join(BASE, "tools", "make_icons_v2.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

APPS = [
 ("PhotoAdobado","/home/smouj/PhotoAdobado-standalone","photo","#FF5C5C"),
 ("ArtAdobado","/home/smouj/adobado-import/ArtAdobado","art","#E85AC8"),
 ("FilmAdobado","/home/smouj/adobado-import/FilmAdobado","film","#FF9F43"),
 ("EffectAdobado","/home/smouj/adobado-import/EffectAdobado","effect","#9B7BFF"),
 ("LightAdobado","/home/smouj/adobado-import/LightAdobado","light","#FFE066"),
 ("SoundAdobado","/home/smouj/adobado-import/SoundAdobado","sound","#4DD6E8"),
 ("DesignAdobado","/home/smouj/adobado-import/DesignAdobado","design","#8BE04E"),
 ("PdfAdobado","/home/smouj/adobado-import/PdfAdobado","pdf","#5B8DEF"),
]

def transparent_logo(slug, hue, ink):
    img = Image.new("RGBA", (1024,1024), (0,0,0,0))
    d = ImageDraw.Draw(img)
    mod.glyph(d, slug, hue, ink=ink)
    return img

for app, dest, slug, hue in APPS:
    if not os.path.isdir(dest):
        print("MISSING", app); continue
    png = os.path.join(ICONS, slug + ".png")
    ico = os.path.join(ICONS, slug + ".ico")
    svg = os.path.join(ICONS, "svg", slug + ".svg")
    img = Image.open(png).convert("RGBA")
    ad = os.path.join(dest, "assets", "adobado")
    os.makedirs(ad, exist_ok=True)
    shutil.copy2(png, os.path.join(ad, "icon.png"))
    shutil.copy2(ico, os.path.join(ad, "icon.ico"))
    icon_dir = os.path.join(dest, "assets", "app-icon")
    if os.path.isdir(icon_dir):
        for dp, dn, fns in os.walk(icon_dir):
            dn[:] = [d for d in dn if d not in ("target",".git")]
            for fn in fns:
                p = os.path.join(dp, fn); low = fn.lower()
                if low.endswith(".png"):
                    size = None
                    if "-1024" in low: size = 1024
                    elif "macos-512" in low: size = 512
                    else:
                        m = re.search(r"(\d+)x(\d+)", dp + "/" + fn)
                        if m: size = int(m.group(1))
                    if size: img.resize((size,size), Image.LANCZOS).save(p)
                elif low.endswith(".ico"):
                    img.save(p, sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
                elif low.endswith(".svg"):
                    shutil.copy2(svg, p)
        open(os.path.join(icon_dir,"README.md"),"w",encoding="utf-8").write("# " + app + " app icon\n\nFamilia Adobado Kit v2 (SMOUJ013, 2026).\nLicencia: MIT OR Apache-2.0.\n")
    brand = os.path.join(dest, "docs", "brand")
    if os.path.isdir(brand):
        transparent_logo(slug, hue, (11,14,19,255)).save(os.path.join(brand,"adobado-logo.png"))
        transparent_logo(slug, hue, (238,242,246,255)).save(os.path.join(brand,"adobado-logo-white.png"))
    subprocess.run(["git","add","-A"], cwd=dest, check=True)
    subprocess.run(["git","-c","user.name=smouj","-c","user.email=hecpoley11@gmail.com","commit","-qm","Apply Adobado icon family v2"], cwd=dest, check=True)
    p = subprocess.run(["git","push","-q","origin","main"], cwd=dest, capture_output=True, text=True)
    print(app, "push", p.returncode, (p.stderr or "")[-100:].replace("\n"," "))
