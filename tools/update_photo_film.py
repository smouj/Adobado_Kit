import io, os, shutil

KIT = "/home/smouj/.openclaw/workspace/infest/apps/adobado-kit"
APPS = [
 ("PhotoAdobado", "/home/smouj/PhotoAdobado-standalone", "/home/smouj/.openclaw/workspace/infest/.openclaw/tmp/photoadobado.png"),
 ("FilmAdobado", "/home/smouj/adobado-import/FilmAdobado", "/home/smouj/.openclaw/workspace/infest/.openclaw/tmp/filmadobado.png"),
]

def edit(path, pairs):
    t = io.open(path, encoding="utf-8").read()
    for a, b in pairs:
        if a in t:
            t = t.replace(a, b, 1)
        else:
            print("WARN", path, a[:50])
    io.open(path, "w", encoding="utf-8").write(t)

edit(os.path.join(KIT, "README.md"), [
 ("| [PhotoAdobado](https://github.com/smouj/PhotoAdobado) | Editor de imagen local: capas, máscaras, PSD y ajustes. Derivado de PhotoCraft. | Build OK · artifact pendiente |",
  "| [PhotoAdobado](https://github.com/smouj/PhotoAdobado) | Editor de imagen local: capas, máscaras, PSD y ajustes. Derivado de PhotoCraft. | Probada en Windows |"),
 ("| [FilmAdobado](https://github.com/smouj/FilmAdobado) | Edición de vídeo local. Derivado de FilmCraft. | Alpha |",
  "| [FilmAdobado](https://github.com/smouj/FilmAdobado) | Edición de vídeo local. Derivado de FilmCraft. | Probada en Windows |"),
])
edit(os.path.join(KIT, "docs", "APPS.md"), [
 ("| PhotoAdobado | https://github.com/smouj/PhotoAdobado | Build OK · artifact pendiente |",
  "| PhotoAdobado | https://github.com/smouj/PhotoAdobado | Build OK · probada en Windows |"),
 ("| FilmAdobado | https://github.com/smouj/FilmAdobado | Alpha · build pendiente |",
  "| FilmAdobado | https://github.com/smouj/FilmAdobado | Build OK · probada en Windows |"),
])

for app, dest, shot in APPS:
    os.makedirs(os.path.join(dest, "docs"), exist_ok=True)
    if os.path.isfile(shot):
        shutil.copy2(shot, os.path.join(dest, "docs", "screenshot.png"))
    p = os.path.join(dest, "README.md")
    t = io.open(p, encoding="utf-8").read()
    if "docs/screenshot.png" not in t:
        lines = t.split(chr(10))
        lines.insert(1, "![%s](docs/screenshot.png)" % app)
        t = chr(10).join(lines)
    t = t.replace(
      "> **Alpha temprana.** Codigo importado y rebrandeado desde PhotoCraft. Build de Windows y prueba de edicion pendientes. No se presenta como app disponible ni como sustituto profesional.",
      "> **Alpha temprana.** Codigo importado y rebrandeado desde PhotoCraft. Build de Windows correcto y app abierta/probada el 20/10/2026. Falta prueba de edicion real y release.")
    t = t.replace(
      "> **Alpha temprana.** Codigo importado y rebrandeado desde FilmCraft. Build de Windows y prueba de edicion pendientes. No se presenta como app disponible ni como sustituto profesional.",
      "> **Alpha temprana.** Codigo importado y rebrandeado desde FilmCraft. Build de Windows correcto y app abierta/probada el 20/10/2026. Falta prueba de edicion real y release.")
    t = t.replace("- Pendiente: compilar en Windows, probar abrir/editar/exportar y publicar release.",
                  "- Build de Windows: OK. App abierta y probada." + chr(10) + "- Pendiente: probar edicion real y publicar release.")
    io.open(p, "w", encoding="utf-8").write(t)
print("statuses updated")
