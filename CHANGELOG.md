# Changelog — Adobado Kit

## [0.2.0] — 2026-10-20

### Cambiado
- El hub deja de incluir Markdown Studio y XLSX Viewer; solo cubre las apps Adobado.
- Ocho repos standalone, sin forks: PhotoAdobado, ArtAdobado, FilmAdobado, EffectAdobado, LightAdobado, SoundAdobado, DesignAdobado y PdfAdobado.
- Nombres de producto con sufijo Adobado; los crates internos se conservan.
- README y docs/APPS.md con estado Alpha y enlace a cada repo.

### Añadido
- docs/ADOBADO.md, aviso de modificación en NOTICE y rebranding en cada repo.
- tools/import_apps.py para repetir la importación.

### Notas
- Builds de Windows pendientes; ninguna app se marca como disponible.
- PdfAdobado: reintentar la creación del repo si GitHub limita la creación masiva.

## [0.1.0] — 2026-10-20

### Añadido
- Hub de Adobado Kit con landing, catálogo y enlaces a las apps.
- Markdown Studio v1.0.0 integrado en `apps/markdown-studio`.
- XLSX Viewer v1.0.0 integrado en `apps/xlsx-viewer`.
- Marca, paleta, roadmap y documentación de contribución.
- Licencias MIT y avisos de terceros.

### Notas
- El kit no está afiliado a Adobe.
- Las apps son locales, sin cuentas ni telemetría.

[0.1.0]: https://github.com/smouj/Adobado_Kit/releases/tag/v0.1.0
