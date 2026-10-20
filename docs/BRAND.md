# Identidad visual — Adobado Kit

## Una fuente por producto

El pack oficial entregado por @smouj es la fuente de los iconos de Adobado Kit y sus ocho aplicaciones. La sincronización se controla con `python tools/check_brand_assets.py --app-repos-root ../AdobadoRepos`.

| Marca | Recurso | Uso |
|---|---|---|
| Adobado Kit / launcher | `launcher/launcher.png`, `launcher/launcher.ico` | Launcher, icono de ventana, accesos directos e instalador. El diseño oficial es una baldosa 2×2 de cuatro colores con contorno claro. |
| Ocho apps | `assets/icons/{photo,art,film,effect,light,sound,design,pdf}.{png,ico}` | Tabla del hub, tarjetas del launcher, accesos directos y recursos de producto. |
| Apps, render escalable | `assets/icons/svg/*.svg` | Wrapper SVG para los PNG oficiales; conserva compatibilidad con empaquetadores que reciben SVG. La ilustración de origen es raster, no vectorial. |
| Familia | `assets/icons/family.png` | Composición de ocho iconos de app; no sustituye el icono del launcher ni el de PdfAdobado como tipo de archivo. |
| PDF | Icono de documento PDF propio de cada interfaz | Identifica el formato de archivo y puede diferir del icono de la aplicación PdfAdobado. |

Los PNG/ICO originales coinciden byte a byte entre Kit, launcher y repos de apps. Las variantes de tamaño de hicolor e ICNS se generan desde el PNG oficial de 1024 px. Los ficheros SVG de Kit y app son idénticos y llevan el PNG de 512 px incrustado para mantener una única imagen de marca.

## Origen y licencia

La obra fue creada y es propiedad de @smouj. El autor autorizó redistribuirla bajo MIT OR Apache-2.0. El inventario está en [`assets/icons/ATTRIBUTION.md`](../assets/icons/ATTRIBUTION.md) y los textos completos en [`assets/icons/LICENSE-MIT.txt`](../assets/icons/LICENSE-MIT.txt) y [`assets/icons/LICENSE-APACHE.txt`](../assets/icons/LICENSE-APACHE.txt). El ZIP se validó con `SHA256SUMS.txt` antes de sincronizarlo.

Para reproducir la sincronización:

    python tools/sync_official_icons.py --pack-dir <directorio-del-pack> --app-repos-root <directorio-con-los-ocho-repos> --apply

El actualizador solo escribe cuando se pasa `--apply`. La comprobación de paridad es de solo lectura y falla si algún icono oficial falta o difiere.

## Capturas y previews

- `assets/social-preview.png` se compone sobre una captura real de FilmAdobado en Windows, suavemente desenfocada y con una capa de marca. Los ocho iconos y el icono del launcher se cargan desde los mismos PNG canónicos.
- PhotoAdobado, FilmAdobado y SoundAdobado conservan capturas reales de aplicación.
- ArtAdobado, LightAdobado, EffectAdobado, DesignAdobado y PdfAdobado usan tarjetas de marca con el estado de validación indicado. No simulan una interfaz.
- No se debe retocar una captura real para cambiar el icono visible; si una captura histórica lleva un icono previo, se conserva como evidencia de esa versión.

## Paleta de producto

| App | Color oficial |
|---|---|
| PhotoAdobado | `#FF5C5C` |
| ArtAdobado | `#E85AC8` |
| FilmAdobado | `#FF9F43` |
| EffectAdobado | `#9B7BFF` |
| LightAdobado | `#F2C94C` |
| SoundAdobado | `#35C8D8` |
| DesignAdobado | `#7BD957` |
| PdfAdobado | `#4F83E8` |

## Voz y microcopy

- Empieza por la tarea de la persona: editar una foto, montar vídeo, preparar audio o revisar un PDF.
- Describe solo funciones que el repo o una prueba confirmen.
- Distingue compilación, instalación, inicio y trabajo con archivos reales.
- Evita slogans genéricos y repetir ventajas obvias. Menciona el procesamiento local una sola vez y donde esté verificado.
- Mantén los estados de Art, Light, Effect, Design y Pdf como tarjetas de marca mientras no exista una captura validada de su interfaz.
- Español como idioma principal; conserva nombres técnicos en inglés cuando sean más precisos.

## Nombres y aviso

Los nombres de producto son PhotoAdobado, ArtAdobado, FilmAdobado, EffectAdobado, LightAdobado, SoundAdobado, DesignAdobado y PdfAdobado. Los crates y ejecutables pueden conservar nombres upstream para no romper los builds.

Adobado Kit es independiente y no está afiliado, patrocinado ni respaldado por Adobe. Las marcas de terceros pertenecen a sus titulares y solo se mencionan para describir categorías.
