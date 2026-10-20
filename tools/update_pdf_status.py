import io
p="/home/smouj/.openclaw/workspace/infest/apps/adobado-kit/README.md"
t=io.open(p,encoding="utf-8").read()
pairs=[
 ("| [EffectAdobado](https://github.com/smouj/EffectAdobado) | Efectos visuales locales. Derivado de EffectCraft. | Alpha |",
  "| [EffectAdobado](https://github.com/smouj/EffectAdobado) | Efectos visuales locales. Derivado de EffectCraft. | Build OK · artifact pendiente |"),
 ("| [DesignAdobado](https://github.com/smouj/DesignAdobado) | Diseño y composición local. Derivado de DesignCraft. | Alpha |",
  "| [DesignAdobado](https://github.com/smouj/DesignAdobado) | Diseño y composición local. Derivado de DesignCraft. | Build OK · artifact pendiente |"),
 ("| PdfAdobado | PDF local: lectura, edición y organización. Derivado de PdfCraft. | Repo en creación |",
  "| [PdfAdobado](https://github.com/smouj/PdfAdobado) | PDF local: lectura, edición y organización. Derivado de PdfCraft. | Repo creado · build en curso |"),
]
for a,b in pairs:
    if a not in t: print("WARN README", a[:40])
    t=t.replace(a,b,1)
io.open(p,"w",encoding="utf-8").write(t)

p="/home/smouj/.openclaw/workspace/infest/apps/adobado-kit/docs/APPS.md"
t=io.open(p,encoding="utf-8").read()
pairs=[
 ("| EffectAdobado | https://github.com/smouj/EffectAdobado | Alpha · build pendiente |",
  "| EffectAdobado | https://github.com/smouj/EffectAdobado | Build OK · artifact pendiente |"),
 ("| DesignAdobado | https://github.com/smouj/DesignAdobado | Alpha · build pendiente |",
  "| DesignAdobado | https://github.com/smouj/DesignAdobado | Build OK · artifact pendiente |"),
 ("| PdfAdobado | Pendiente · límite temporal de GitHub | Repo en creación |",
  "| PdfAdobado | https://github.com/smouj/PdfAdobado | Repo creado · build en curso |"),
]
for a,b in pairs:
    if a not in t: print("WARN APPS", a[:40])
    t=t.replace(a,b,1)
io.open(p,"w",encoding="utf-8").write(t)

p="/home/smouj/.openclaw/workspace/infest/apps/adobado-kit/index.html"
t=io.open(p,encoding="utf-8").read()
t=t.replace('<div class="tag alpha">Build en curso</div>','<div class="tag alpha">Build OK · artifact pendiente</div>')
t=t.replace('<div class="tag plan">Repo en creación</div>','<div class="tag alpha">Build en curso</div>')
t=t.replace('<div class="links"><a href="docs/APPS.md">Ficha</a><span class="muted">Repo en creación</span></div>','<div class="links"><a href="https://github.com/smouj/PdfAdobado">Ver repo</a><a class="muted" href="docs/APPS.md">Ficha</a></div>')
t=t.replace("Photo, Film y Sound ya abren en Windows; Art y Light tienen build OK; Effect y Design siguen compilando.","Photo, Film y Sound ya abren en Windows; Art, Light, Effect y Design tienen build OK; Pdf está compilando.")
io.open(p,"w",encoding="utf-8").write(t)
print("kit statuses updated")
