import io, os, shutil

KIT = "/home/smouj/.openclaw/workspace/infest/apps/adobado-kit"
SOUND = "/home/smouj/adobado-import/SoundAdobado"
SHOT = "/home/smouj/.openclaw/workspace/infest/.openclaw/tmp/sound_window.png"

def edit(path, pairs):
    t = io.open(path, encoding="utf-8").read()
    for a, b in pairs:
        if a in t:
            t = t.replace(a, b, 1)
        else:
            print("WARN missing in", path, ":", a[:60])
    io.open(path, "w", encoding="utf-8").write(t)

edit(os.path.join(KIT, "README.md"), [
    ("| [PhotoAdobado](https://github.com/smouj/PhotoAdobado) | Editor de imagen local: capas, máscaras, PSD y ajustes. Derivado de PhotoCraft. | Alpha |",
     "| [PhotoAdobado](https://github.com/smouj/PhotoAdobado) | Editor de imagen local: capas, máscaras, PSD y ajustes. Derivado de PhotoCraft. | Build OK · artifact pendiente |"),
    ("| [LightAdobado](https://github.com/smouj/LightAdobado) | Revelado y color local. Derivado de LightCraft. | Alpha |",
     "| [LightAdobado](https://github.com/smouj/LightAdobado) | Revelado y color local. Derivado de LightCraft. | Build OK · artifact pendiente |"),
    ("| [SoundAdobado](https://github.com/smouj/SoundAdobado) | Edición de audio local. Derivado de SoundCraft. | Alpha |",
     "| [SoundAdobado](https://github.com/smouj/SoundAdobado) | Edición de audio local. Derivado de SoundCraft. | Probada en Windows |"),
])

edit(os.path.join(KIT, "docs", "APPS.md"), [
    ("| PhotoAdobado | https://github.com/smouj/PhotoAdobado | Alpha · build pendiente |",
     "| PhotoAdobado | https://github.com/smouj/PhotoAdobado | Build OK · artifact pendiente |"),
    ("| LightAdobado | https://github.com/smouj/LightAdobado | Alpha · build pendiente |",
     "| LightAdobado | https://github.com/smouj/LightAdobado | Build OK · artifact pendiente |"),
    ("| SoundAdobado | https://github.com/smouj/SoundAdobado | Alpha · build pendiente |",
     "| SoundAdobado | https://github.com/smouj/SoundAdobado | Build OK · probada en Windows |"),
])

os.makedirs(os.path.join(SOUND, "docs"), exist_ok=True)
if os.path.isfile(SHOT):
    shutil.copy2(SHOT, os.path.join(SOUND, "docs", "screenshot.png"))

p = os.path.join(SOUND, "README.md")
t = io.open(p, encoding="utf-8").read()
if "docs/screenshot.png" not in t:
    lines = t.split(chr(10))
    lines.insert(1, "![SoundAdobado](docs/screenshot.png)")
    t = chr(10).join(lines)
t = t.replace(
    "> **Alpha temprana.** Codigo importado y rebrandeado desde SoundCraft. Build de Windows y prueba de edicion pendientes. No se presenta como app disponible ni como sustituto profesional.",
    "> **Alpha temprana.** Codigo importado y rebrandeado desde SoundCraft. Build de Windows correcto y app abierta/probada el 20/10/2026. Falta release y prueba de edicion de audio real.")
t = t.replace(
    "- Pendiente: compilar en Windows, probar abrir/editar/exportar y publicar release.",
    "- Build de Windows: OK. App abierta y probada." + chr(10) + "- Pendiente: probar edicion de audio real y publicar release.")
io.open(p, "w", encoding="utf-8").write(t)
print("status docs updated")
