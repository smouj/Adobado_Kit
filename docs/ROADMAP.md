# Roadmap — Adobado Kit

El kit crece por herramientas completas, no por promesas. Una app pasa a `Disponible` cuando abre, edita y exporta de verdad, sin depender de la nube.

## v0.1.0 — Hub y primeras apps

- Hub de Adobado Kit con landing, catálogo y enlaces.
- Markdown Studio v1.0.0.
- XLSX Viewer v1.0.0.
- Marca, licencias y documentación.

## v0.2.0 — Ocho repos standalone

- Hub solo con apps Adobado; Markdown Studio y XLSX Viewer salen del kit.
- Repos standalone, no forks: PhotoAdobado, ArtAdobado, FilmAdobado, EffectAdobado, LightAdobado, SoundAdobado, DesignAdobado, PdfAdobado.
- Rebranding visible, licencias y docs/ADOBADO.md en cada repo.
- Estado Alpha: builds de Windows y pruebas de edición pendientes.
- PdfAdobado: reintentar la creación del repo si GitHub aplica su límite temporal.

## v0.2.1 — PhotoAdobado

- Build de Windows y prueba abrir -> editar -> exportar.
- Iconos definitivos y release solo con binario probado.

## v0.3.0 — ArtAdobado

- Lienzo SVG con zoom y cuadrícula.
- Formas, trazos, texto y edición de nodos.
- Importar/exportar SVG limpio.
- Sin efectos rasterizados en la primera versión.

## v0.4.0 — FilmAdobado

- Importar vídeo local y timeline.
- Corte, orden y subtítulos.
- Exportación local (WebCodecs o ffmpeg opcional).
- Sin streaming ni subida de archivos.

## v0.5.0 — SoundAdobado

- Forma de onda y selección.
- Corte, normalización y fundidos.
- Exportación WAV/MP3.
- Sin bibliotecas en la nube.

## v0.6.0 — PdfAdobado

- Unir, separar, rotar y reordenar PDF.
- Composición básica de páginas.
- Exportación local.
- Sin firma digital en la primera versión.

## v0.7.0 — LightAdobado

- Revelado RAW cuando sea viable, empezando por JPEG/PNG.
- Curvas, temperatura, exposición y color.
- Exportación con perfiles básicos.

## Licencias y marcas

- El código upstream es MIT/Apache-2.0 y permite derivados con avisos.
- Los nombres, wordmarks y logos de ArtCraft son trademarks y no están licenciados: se eliminan de las builds.
- Adobe y sus productos son marcas de Adobe Inc. El kit no está afiliado.
- Cada app derivada debe documentar su commit de origen y sus cambios.

## Fuera de alcance

- Cuentas, suscripciones y telemetría.
- Procesamiento en servidores propios.
- Formatos propietarios cerrados sin librería libre verificable.
- Prometer paridad con productos comerciales: el objetivo es resolver tareas reales, no clonar menús.

## Cómo se cierra una app

1. Implementación local con contrato claro.
2. Prueba manual de abrir → editar → exportar.
3. Licencias y créditos revisados.
4. Documentación y captura actualizada.
5. Release con versión y changelog.
