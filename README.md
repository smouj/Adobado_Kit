# Adobado Kit

**Herramientas creativas locales, sin suscripciones y sin nube.**

[![License: MIT](https://img.shields.io/badge/license-MIT-b8f34a)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-6cb6ff)](https://github.com/smouj/Adobado_Kit/releases)
[![Local-first](https://img.shields.io/badge/privacy-100%25%20local-b8f34a)](#principios)
[![Open source](https://img.shields.io/badge/open%20source-MIT-ff7a59)](LICENSE)
[![Apps](https://img.shields.io/badge/apps-8-6cb6ff)](#apps)

Un kit personal de aplicaciones de escritorio para trabajar con tus archivos en tu equipo. Cada app es un repo independiente, funciona sin conexión y no pide cuentas.

> **Adobado Kit no está afiliado a Adobe.** Es un proyecto personal e independiente. Los nombres de productos se usan solo para describir categorías de herramientas.

## Apps

| App | Qué hace | Estado |
|---|---|---|
| [PhotoAdobado](https://github.com/smouj/PhotoAdobado) | Editor de imagen local: capas, máscaras, PSD y ajustes. Derivado de PhotoCraft. | Build OK · artifact pendiente |
| [ArtAdobado](https://github.com/smouj/ArtAdobado) | Arte vectorial y SVG local. Derivado de VectorCraft. | Alpha |
| [FilmAdobado](https://github.com/smouj/FilmAdobado) | Edición de vídeo local. Derivado de FilmCraft. | Alpha |
| [EffectAdobado](https://github.com/smouj/EffectAdobado) | Efectos visuales locales. Derivado de EffectCraft. | Alpha |
| [LightAdobado](https://github.com/smouj/LightAdobado) | Revelado y color local. Derivado de LightCraft. | Build OK · artifact pendiente |
| [SoundAdobado](https://github.com/smouj/SoundAdobado) | Edición de audio local. Derivado de SoundCraft. | Probada en Windows |
| [DesignAdobado](https://github.com/smouj/DesignAdobado) | Diseño y composición local. Derivado de DesignCraft. | Alpha |
| PdfAdobado | PDF local: lectura, edición y organización. Derivado de PdfCraft. | Repo en creación |

El catálogo con commits, licencias y estado real está en [docs/APPS.md](docs/APPS.md).

## Estado

Las ocho apps tienen código importado y rebrandeado, pero **ninguna se marca como disponible**: falta compilar en Windows y probar abrir, editar y exportar. Hasta entonces el estado es Alpha y no se publican binarios.

Cada repo conserva LICENSE, NOTICE y ATTRIBUTION del upstream. ArtCraft, PhotoCraft, VectorCraft y compañía son marcas del ArtCraft Team y no están cubiertas por la licencia de código; se retiran de las distribuciones.

## Principios

1. **Local primero.** Tus archivos no salen del equipo. Sin cuentas, servidores ni telemetría.
2. **Abierto de verdad.** Código MIT/Apache, dependencias auditables y formatos estándar.
3. **Herramientas honestas.** Cada app dice qué hace, qué no hace y en qué estado está.

## Uso

- Abre el hub en [index.html](index.html) o en https://smouj.github.io/Adobado_Kit/.
- Cada app se descarga y compila desde su propio repositorio.
- No hay instalador ni backend en el hub: es HTML estático.

## Estructura

    Adobado_Kit/
    ├─ index.html                 # hub / landing
    ├─ assets/                    # logo, iconos y capturas
    ├─ docs/
    │  ├─ APPS.md                 # catálogo y estado real
    │  ├─ ROADMAP.md
    │  ├─ BRAND.md
    │  └─ UPSTREAM.md             # auditoría de ArtCraft
    ├─ tools/
    │  ├─ import_apps.py          # importación y rebranding
    │  └─ sync-upstream.sh
    ├─ LICENSE
    └─ THIRD_PARTY_NOTICES.md

## Desarrollo

El hub es HTML, CSS y JavaScript sin frameworks. Las apps son proyectos Rust independientes; sus repos contienen sus propias instrucciones de build.

## Licencia

MIT para el código del hub. Cada app conserva las licencias de su upstream. Consulta [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Hecho por [SMOUJ013](https://github.com/smouj).
