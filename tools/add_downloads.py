import io
p="/home/smouj/.openclaw/workspace/infest/apps/adobado-kit/README.md"
t=io.open(p,encoding="utf-8").read()
marker="## Apps"
section="""## Descargas

- **Launcher + instalador:** [AdobadoKit-Launcher-v0.3.0.zip](https://github.com/smouj/Adobado_Kit/releases/download/v0.3.0/AdobadoKit-Launcher-v0.3.0.zip). Abre o instala las apps, crea accesos directos y no requiere administrador.
- **Wallpapers:** [AdobadoKit-Wallpapers-v1.0.zip](https://github.com/smouj/Adobado_Kit/releases/download/v0.3.0/AdobadoKit-Wallpapers-v1.0.zip). Tres variantes en 16:9, 21:9, 16:10, 4:3 y móvil.

"""
if "## Descargas" not in t:
    t=t.replace(marker, section+marker, 1)
io.open(p,"w",encoding="utf-8").write(t)

p="/home/smouj/.openclaw/workspace/infest/apps/adobado-kit/index.html"
t=io.open(p,encoding="utf-8").read()
if 'id="descargas"' not in t:
    nav='<a href="#apps">Apps</a>'
    t=t.replace(nav, '<a href="#descargas">Descargas</a>\n      '+nav, 1)
    section='''  <section id="descargas">
    <div class="wrap">
      <div class="banner">
        <div>
          <h2>Launcher y wallpapers</h2>
          <p>Descarga el launcher para abrir o instalar las apps, y el pack de wallpapers para escritorio, tablet y móvil.</p>
        </div>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
          <a class="button primary" href="https://github.com/smouj/Adobado_Kit/releases/download/v0.3.0/AdobadoKit-Launcher-v0.3.0.zip">Launcher (.zip)</a>
          <a class="button ghost" href="https://github.com/smouj/Adobado_Kit/releases/download/v0.3.0/AdobadoKit-Wallpapers-v1.0.zip">Wallpapers (.zip)</a>
        </div>
      </div>
    </div>
  </section>

'''
    t=t.replace('  <section id="apps">', section+'  <section id="apps">',1)
io.open(p,"w",encoding="utf-8").write(t)
print("downloads added")
