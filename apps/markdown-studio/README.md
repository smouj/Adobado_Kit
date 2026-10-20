# Markdown Studio

Editor y visor **local** de Markdown para Windows. Escribe a la izquierda, mira el resultado a la derecha y guarda tus documentos sin subirlos a ningún servidor.

## Características

- **GFM completo**: tablas, listas de tareas, tachado, citas, enlaces automáticos y bloques de código.
- **Resaltado de sintaxis** con Highlight.js.
- **Vista dividida** con divisor arrastrable, solo editor o solo vista previa.
- **Autoguardado local** en el navegador y restauración del borrador.
- **Abrir, guardar y exportar**: archivos `.md`, exportación a HTML independiente e impresión a PDF.
- **Índice** generado desde los encabezados.
- **Temas oscuro y claro**, tipografía de lectura y barra de estado con palabras, líneas y cursor.
- **100 % local**: sin backend, sin cuentas y sin peticiones de red.

## Uso

- Abre el acceso directo **Editor Markdown** del escritorio o `launcher.vbs`.
- Escribe Markdown en el panel izquierdo; la vista previa se actualiza sola.
- Arrastra un archivo `.md` o pulsa **Abrir**.
- **Guardar** escribe el archivo; **HTML** exporta una página autónoma.
- `Ctrl+B`, `Ctrl+I`, `Ctrl+K`, `Ctrl+S` y `Ctrl+O` funcionan como esperas.

| Atajo | Acción |
|---|---|
| `Ctrl+B` | Negrita |
| `Ctrl+I` | Cursiva |
| `Ctrl+K` | Enlace |
| `Ctrl+S` | Guardar |
| `Ctrl+O` | Abrir |
| `Tab` | Insertar dos espacios |

## Privacidad

El texto se procesa con JavaScript en tu equipo. El borrador se guarda en `localStorage`; no hay analíticas, cookies de terceros ni subida de archivos. Los enlaces e imágenes remotos solo se cargan si el documento los incluye y decides abrirlo.

## Estructura

- `index.html` — editor, vista previa y estilos.
- `vendor/marked.min.js` — parser Markdown (MIT).
- `vendor/purify.min.js` — saneado del HTML (Apache-2.0).
- `vendor/highlight.min.js` y `vendor/github-dark.min.css` — resaltado (BSD-3-Clause).
- `launcher.vbs` — ventana de app con Chrome o Edge.
- `app.ico` — icono del acceso directo.

## Desarrollo

No hay build ni dependencias instalables: HTML, CSS y JavaScript sin frameworks. Abre `index.html` o usa `?demo=1` para cargar la demostración y `?theme=light` para el tema claro.

## Licencias

Código del editor: MIT. Las librerías de `vendor/` conservan sus licencias originales; consulta `THIRD_PARTY_NOTICES.md`.
