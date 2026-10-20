# Identidad visual — Adobado Kit

## Marcas y funciones

El kit reúne ocho aplicaciones con iconos propios y conserva una marca independiente para el hub y otra para el launcher. No son variantes intercambiables.

| Archivo o familia | Función |
|---|---|
| assets/logo.svg | Marca de Adobado Kit: dos formas de color y una barra lima. Se usa en el hub, favicon y documentación del kit. |
| launcher/launcher.svg y launcher/launcher.ico | Icono del launcher: cuadrícula 3×3 con los ocho colores de la familia y borde lima. |
| assets/icons/svg/*.svg | Fuente SVG canónica de cada aplicación. |
| assets/icons/*.png e *.ico | Iconos de producto usados en la tabla del hub y el launcher. |
| assets/icons/family.png | Vista conjunta de los ocho iconos; es una lámina de familia, no un icono de aplicación o del launcher. |
| PDF document icon | Icono de tipo de archivo PDF en la interfaz; es intencionalmente distinto del icono de PdfAdobado. |

## Iconos de aplicación

Cada app tiene una identidad visual propia. Dentro de una misma app, el icono debe coincidir en el README, la ficha del hub, la tarjeta del launcher, el ejecutable, los accesos directos y los instaladores.

El PNG e ICO de cada app se sincronizan byte por byte entre el kit y el launcher, y con los archivos de producto del repo de la app. El SVG canónico también coincide con el SVG de aplicación correspondiente. El launcher conserva su cuadrícula 3×3 en launcher/launcher.ico, launcher/icons/launcher.ico y los iconos del instalador.

Comprueba la sincronización desde la raíz del kit:

    python tools/check_brand_assets.py --app-repos-root ../apps

El argumento opcional debe apuntar a una carpeta que contenga los repos PhotoAdobado, ArtAdobado, FilmAdobado, EffectAdobado, LightAdobado, SoundAdobado, DesignAdobado y PdfAdobado. El script informa de cada paridad y falla si falta un archivo o difieren sus bytes.

Los binarios de las releases también deben comprobarse después de compilar. Las releases alpha públicas de PhotoAdobado, FilmAdobado y SoundAdobado son anteriores a la identidad visual actual y conservan el icono previo; la actualización del código fuente no modifica un ZIP ya publicado.

## Presentación

- La imagen social del kit parte de una captura real de FilmAdobado en Windows, suavemente desenfocada, con la marca del kit, los ocho iconos y una etiqueta que identifica la captura.
- Las tarjetas de marca de ArtAdobado, LightAdobado, EffectAdobado, DesignAdobado y PdfAdobado son piezas de identidad, no capturas de su interfaz. Incluyen el estado de validación actual.
- No presentar mockups o tarjetas de marca como capturas reales. Mantener texto alternativo descriptivo y captions que identifiquen la app.
- Los pantallazos de PhotoAdobado, FilmAdobado y SoundAdobado son capturas de aplicación y deben mantenerse separados de la imagen social con desenfoque.

## Paleta

| Token | Hex | Uso |
|---|---|---|
| Ink | #080a0e | Fondo principal |
| Panel | #11151c | Superficies |
| Line | #252c37 | Bordes |
| Text | #eef2f6 | Texto |
| Muted | #98a3b1 | Texto secundario |
| Coral | #ff7a59 | Acento cálido |
| Blue | #6cb6ff | Acento técnico |
| Lime | #b8f34a | Acción y disponibilidad |
| Cream | #f2e9dc | Acento editorial |

## Voz

- Directa, técnica y sin hype.
- Español como idioma principal; términos técnicos en inglés cuando ayudan a la precisión.
- Cada app describe lo que hace y su etapa real.
- No afirmar paridad con otros productos ni usar su identidad visual.

## Nombres y aviso

Los nombres de producto terminan en Adobado: PhotoAdobado, ArtAdobado, FilmAdobado, EffectAdobado, LightAdobado, SoundAdobado, DesignAdobado y PdfAdobado. Los crates pueden conservar los nombres upstream para evitar romper los builds.

Adobado Kit es un proyecto independiente y no está afiliado, patrocinado ni respaldado por Adobe. Las marcas de terceros pertenecen a sus titulares y se mencionan solo para describir categorías.
