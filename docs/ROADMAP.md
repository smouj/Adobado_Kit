# Roadmap — Adobado Kit

## Estado actual — 20 de octubre de 2026

La versión v0.3.2 del launcher y el pack de wallpapers está publicada. El launcher usa una cuadrícula 3×3 con borde lima; el instalador opcional no requiere permisos de administrador. El pack contiene 33 wallpapers para varios formatos de pantalla.

Las ocho apps pasan el workflow de compilación para Windows. PhotoAdobado, FilmAdobado y SoundAdobado se instalaron y abrieron manualmente; cinco apps siguen pendientes de instalación e inicio manual. En las ocho queda pendiente validar un flujo de abrir, modificar y exportar un archivo real.

Hay releases alpha para Photo, Film y Sound. Sus paquetes se generaron antes de la actualización de iconos y conservan la identidad anterior. Art, Light, Effect, Design y Pdf todavía no tienen releases. Los estados detallados y los enlaces a Actions están en [APPS.md](APPS.md).

## Siguientes pasos

1. Instalar y abrir ArtAdobado, LightAdobado, EffectAdobado, DesignAdobado y PdfAdobado en Windows.
2. Ejecutar una prueba de archivo real de principio a fin en cada aplicación, incluidas Photo, Film y Sound.
3. Compilar y probar los binarios con los iconos actuales; actualizar las tres releases alpha solo después de validar la identidad integrada y el flujo funcional.
4. Preparar una primera release para las otras apps solo cuando superen el mismo criterio.
5. Mantener la documentación, las capturas, los metadatos sociales y la paridad de iconos sincronizados en cada cambio.

## Requisitos antes de publicar una descarga

- Build correcto para Windows.
- Instalación e inicio manual comprobados.
- Flujo de abrir, modificar y exportar comprobado con un archivo real.
- Icono del binario igual al oficial de la app.
- Licencias, avisos, captura, README y changelog revisados.
- Release con versión, artefacto y notas coincidentes.

## Información para quien descarga

- Indicar en cada ficha dónde se procesan los archivos y qué formatos admite la app.
- Mantener visibles las licencias, dependencias y avisos de terceros.
- Identificar las tarjetas de marca como piezas gráficas; no presentarlas como capturas de interfaz.
- Describir las herramientas por sus funciones, sin compararlas con productos comerciales.
