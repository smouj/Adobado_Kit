#!/usr/bin/env python3
import os, re, subprocess, sys, shutil, time

OWNER = "smouj"
KIT = "https://github.com/smouj/Adobado_Kit"
ROOT = "/home/smouj/adobado-import"

APPS = [
    ("ArtAdobado", "vectorcraft", "VectorCraft", "9e7929ee8966977e6daf200f457c570f7aaf7c51", "Arte vectorial local", "vector, svg, design"),
    ("FilmAdobado", "filmcraft", "FilmCraft", "fb4cbda47a134eedabd89fe02cd59ebc69462737", "Edicion de video local", "video, editor, film"),
    ("EffectAdobado", "effectcraft", "EffectCraft", "ef74d82902ba486891b02afa87e42963cc9b84cc", "Efectos visuales locales", "vfx, effects, video"),
    ("LightAdobado", "lightcraft", "LightCraft", "d999e382bafbb5d5c54482fdb1d11f6a63bfdf69", "Revelado y color local", "photo, raw, color"),
    ("SoundAdobado", "soundcraft", "SoundCraft", "25d52c646aea780c8076ff966076f994ad256221", "Audio local", "audio, sound, editor"),
    ("DesignAdobado", "designcraft", "DesignCraft", "443ea4640ca368fcf0241b04813bd3817acd5df8", "Diseno y composicion local", "design, layout, publishing"),
    ("PdfAdobado", "pdfcraft", "PdfCraft", "ec0a965074f376a5bf610435948e4e5184bf3299", "PDF local", "pdf, documents, editor"),
]

README_T = """# {name}

**{tagline}.** Derivado de {product}, rebrandeado para Adobado Kit.

[![License](https://img.shields.io/badge/license-{license_badge}-6cb6ff)](LICENSE-APACHE)
[![Rust](https://img.shields.io/badge/Rust-1.95%2B-ff7a59)](Cargo.toml)
[![Status](https://img.shields.io/badge/status-early%20alpha-d69e2e)](#estado)
[![Adobado Kit](https://img.shields.io/badge/Adobado%20Kit-hub-b8f34a)]({kit})

> **Alpha temprana.** Codigo importado y rebrandeado desde {product}. Build de Windows y prueba de edicion pendientes. No se presenta como app disponible ni como sustituto profesional.
>
> Proyecto independiente. No afiliado a ArtCraft ni a Adobe.

## Estado

- Codigo fuente: importado desde {upstream} en el commit {sha}.
- Rebranding visible: nombre, enlaces, README, avisos y documentacion.
- Pendiente: compilar en Windows, probar abrir/editar/exportar y publicar release.

## Build

Requisitos: Rust 1.95 o superior.

    cargo build --release -p {package}

El nombre interno del crate se conserva para no romper el workspace; el nombre de producto visible es {name}.

## Procedencia y licencias

- Upstream: {upstream_url}
- Commit base: {sha}
- Licencia: {license_long}. Se conservan los archivos de licencia, NOTICE y ATTRIBUTION del upstream.
- Cambios: docs/ADOBADO.md.
- La marca, el wordmark y los logos de ArtCraft no estan cubiertos por la licencia y se retiran de la distribucion.

## Adobado Kit

Este repo forma parte de Adobado Kit: {kit}

Hecho por @smouj.
"""

ADOBADO_T = """# {name} - procedencia y cambios

## Origen

- Upstream: {upstream_url}
- Commit base: {sha}
- Licencia: {license_long}
- Copyright original: ArtCraft Team and the {product} contributors.

## Cambios de esta distribucion

- Nombre de producto visible: {name} (el crate y el ejecutable internos se conservan para no romper el build).
- Enlaces de ayuda, GitHub e issues apuntando a {repo_url} y a Adobado Kit.
- README propio, CHANGELOG y guia de contribucion.
- Se retiran los logos y assets de marca de ArtCraft incluidos en docs/brand.
- No se han cambiado el motor, los formatos ni las funciones de edicion.

## Pendiente

- Rebranding de iconos de aplicacion.
- Build de Windows y prueba de abrir, editar y exportar.
- Release solo cuando exista un binario probado.

## Marcas

ArtCraft, {product} y sus logos son marcas del ArtCraft Team y no estan cubiertos por la licencia de codigo. Adobe y sus productos son marcas de Adobe Inc. Este proyecto no esta afiliado a Adobe ni a ArtCraft.

## Aviso

Esta es una distribucion modificada. Las modificaciones son de @smouj (2026). El codigo original conserva sus avisos de copyright y licencia.
"""

CHANGELOG_T = """# Changelog - {name}

## 0.1.0-alpha.1 - 2026-10-20

### Anadido
- Importacion del codigo de {product} en el commit {sha}.
- Rebranding visible: {name}, enlaces, README, ADOBADO.md y avisos.
- Documentacion de procedencia y contribucion.

### Conservado
- Archivos de licencia, NOTICE y ATTRIBUTION del upstream.
- Motor, formatos y funciones de edicion.

### Notas
- Alpha temprana. Build de Windows pendiente. No es una app disponible.
"""

CONTRIB_T = """# Contribuir - {name}

{name} es un derivado de {product}. Antes de enviar cambios:

1. Conserva las licencias y los avisos de procedencia.
2. No introduzcas marcas, logos o assets de ArtCraft.
3. Prueba abrir, editar y exportar en local.
4. Documenta el cambio en CHANGELOG.md y ADOBADO.md.

Para cambios de marca o producto, coordina con Adobado Kit: {kit}
"""

def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and p.returncode != 0:
        raise RuntimeError("CMD FAILED: %s\n%s\n%s" % (" ".join(cmd), p.stdout[-2000:], p.stderr[-2000:]))
    return p

def package_name(dest):
    apps = os.path.join(dest, "apps")
    if not os.path.isdir(apps):
        return "app"
    for d in sorted(os.listdir(apps)):
        cargo = os.path.join(apps, d, "Cargo.toml")
        if not os.path.isfile(cargo):
            continue
        text = open(cargo, encoding="utf-8", errors="replace").read()
        m = re.search(r'default-run\s*=\s*"([^"]+)"', text) or re.search(r'(?m)^name\s*=\s*"([^"]+)"', text)
        if m:
            return m.group(1)
    return "app"

def licenses(dest):
    mit = os.path.isfile(os.path.join(dest, "LICENSE-MIT"))
    apache = os.path.isfile(os.path.join(dest, "LICENSE-APACHE"))
    if mit and apache:
        return "MIT OR Apache-2.0", "MIT%20OR%20Apache--2.0", "MIT OR Apache-2.0"
    if mit:
        return "MIT", "MIT", "MIT"
    return "Apache-2.0", "Apache--2.0", "Apache-2.0"

def rebrand(dest, name, upstream, product):
    exts = (".rs", ".toml", ".tsv", ".md", ".ps1", ".sh", ".json", ".txt", ".yml", ".yaml")
    skip = {"NOTICE", "ATTRIBUTION.md", "LICENSE", "LICENSE-MIT", "LICENSE-APACHE", "LICENSE-APACHE-2.0"}
    for base in ("apps", "crates", "packaging", "xtask", "docs", "tools"):
        root = os.path.join(dest, base)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in ("target", ".git", "brand")]
            for fn in filenames:
                if fn in skip or not fn.endswith(exts):
                    continue
                path = os.path.join(dirpath, fn)
                try:
                    text = open(path, encoding="utf-8", errors="replace").read()
                except Exception:
                    continue
                original = text
                text = text.replace(product, name)
                text = text.replace("ArtCraft", "Adobado Kit")
                text = text.replace("https://getartcraft.com/apps/" + upstream, "https://github.com/smouj/" + name)
                text = text.replace("https://getartcraft.com", KIT)
                text = text.replace("https://github.com/storytold/" + upstream, "https://github.com/smouj/" + name)
                text = text.replace("https://discord.gg/artcraft", KIT)
                if text != original:
                    open(path, "w", encoding="utf-8").write(text)

def process(name, upstream, product, sha, tagline, topics):
    dest = os.path.join(ROOT, name)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    run(["git", "clone", "--depth", "1", "https://github.com/storytold/%s.git" % upstream, dest], cwd=ROOT)
    sha = run(["git", "rev-parse", "HEAD"], dest).stdout.strip()
    rebrand(dest, name, upstream, product)
    pkg = package_name(dest)
    lic_long, lic_badge, _ = licenses(dest)
    upstream_url = "https://github.com/storytold/" + upstream
    repo_url = "https://github.com/%s/%s" % (OWNER, name)
    open(os.path.join(dest, "README.md"), "w", encoding="utf-8").write(README_T.format(
        name=name, tagline=tagline, product=product, package=pkg, sha=sha,
        upstream=upstream, upstream_url=upstream_url, repo_url=repo_url,
        kit=KIT, license_badge=lic_badge, license_long=lic_long))
    os.makedirs(os.path.join(dest, "docs"), exist_ok=True)
    open(os.path.join(dest, "docs", "ADOBADO.md"), "w", encoding="utf-8").write(ADOBADO_T.format(
        name=name, product=product, sha=sha, upstream_url=upstream_url,
        repo_url=repo_url, license_long=lic_long))
    open(os.path.join(dest, "CHANGELOG.md"), "w", encoding="utf-8").write(CHANGELOG_T.format(
        name=name, product=product, sha=sha))
    open(os.path.join(dest, "CONTRIBUTING.md"), "w", encoding="utf-8").write(CONTRIB_T.format(
        name=name, product=product, kit=KIT))
    for junk in (".github", os.path.join("docs", "brand")):
        p = os.path.join(dest, junk)
        if os.path.isdir(p):
            shutil.rmtree(p)
    # marca de modificacion en NOTICE
    notice = os.path.join(dest, "NOTICE")
    if os.path.isfile(notice):
        with open(notice, "a", encoding="utf-8") as f:
            f.write("\n\nModifications - %s\nThis repository is a modified derivative of %s, maintained by @smouj.\nChanges: product naming, visible branding, help links, README and documentation.\nNo ArtCraft name, wordmark or logo is used in this distribution.\nThe original code remains under its upstream license.\n" % (name, product))
    # historia propia: un solo commit raiz
    run(["git", "checkout", "-q", "--orphan", "adobado-main"], dest)
    run(["git", "add", "-A"], dest)
    run(["git", "-c", "user.name=smouj", "-c", "user.email=hecpoley11@gmail.com", "commit", "-q", "-m", "%s 0.1.0-alpha.1: rebranded %s derivative" % (name, product)], dest)
    run(["git", "branch", "-D", "main"], dest, check=False)
    run(["git", "branch", "-M", "main"], dest)
    run(["git", "remote", "rename", "origin", "upstream"], dest, check=False)
    # repo en GitHub
    view = run(["gh", "repo", "view", "%s/%s" % (OWNER, name)], check=False)
    if view.returncode != 0:
        run(["gh", "repo", "create", "%s/%s" % (OWNER, name), "--public", "--source", ".", "--remote", "origin", "--push",
             "--description", "%s: %s, derivado de %s. Parte de Adobado Kit. Alpha temprana." % (name, tagline, product)], dest)
    else:
        run(["git", "remote", "add", "origin", repo_url], dest, check=False)
        run(["git", "push", "-u", "origin", "main", "--force"], dest)
    topic_args = []
    for t in ["rust", "local-first", "open-source", "windows", "adobado-kit", "alpha"] + topics.split(", "):
        topic_args += ["--add-topic", t.strip()]
    run(["gh", "repo", "edit", "%s/%s" % (OWNER, name), "--description",
         "%s: %s, derivado de %s. Parte de Adobado Kit. Alpha temprana." % (name, tagline, product),
         "--homepage", KIT] + topic_args, check=False)
    print("OK %s pkg=%s license=%s" % (name, pkg, lic_long), flush=True)

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for app in APPS:
        if only and app[0] != only:
            continue
        try:
            process(*app)
        except Exception as e:
            print("FAIL %s: %s" % (app[0], str(e)[:2000]), flush=True)
