# Upstream — ArtCraft

Adobado Kit usa ArtCraft como referencia de código para las futuras apps de categoría Adobe. No es un fork del hub: cada app se integrará como derivado independiente, con su licencia, su aviso de procedencia y su propia marca.

## Auditoría

| Repo upstream | App de referencia | Licencia | Commit fijado | Estado |
|---|---|---|---|---|
| storytold/photocraft | PhotoCraft | MIT OR Apache-2.0 | 03d0c7e3b39cfb401cdbba590431141ee4c6c8fa | Clonado y auditado (69 MB) |
| storytold/vectorcraft | VectorCraft | Apache-2.0 | 9e7929ee8966977e6daf200f457c570f7aaf7c51 | Referencia |
| storytold/filmcraft | FilmCraft | Apache-2.0 | fb4cbda47a134eedabd89fe02cd59ebc69462737 | Referencia |
| storytold/effectcraft | EffectCraft | Apache-2.0 | ef74d82902ba486891b02afa87e42963cc9b84cc | Referencia |
| storytold/lightcraft | LightCraft | Apache-2.0 | d999e382bafbb5d5c54482fdb1d11f6a63bfdf69 | Referencia |
| storytold/soundcraft | SoundCraft | Apache-2.0 | 25d52c646aea780c8076ff966076f994ad256221 | Referencia |
| storytold/designcraft | DesignCraft | Apache-2.0 | 443ea4640ca368fcf0241b04813bd3817acd5df8 | Referencia |
| storytold/pdfcraft | PdfCraft | Apache-2.0 | ec0a965074f376a5bf610435948e4e5184bf3299 | Referencia |

PhotoCraft se declara **early alpha** (v0.10.0) en su propio README. No se presenta como sustituto profesional ni como producto terminado.

## Licencias y marcas

- El código de los repos de ArtCraft es MIT y/o Apache-2.0. Permite uso comercial, modificación y redistribución si se conservan los avisos y licencias.
- El nombre **ArtCraft**, su wordmark y sus logos son marcas del ArtCraft Team y **no están cubiertos por la licencia**. No se usarán en Adobado Kit ni en builds derivadas.
- PhotoCraft incluye LICENSE-MIT, LICENSE-APACHE, NOTICE y ATTRIBUTION.md. Hay que conservarlos y añadir un aviso de cambios.
- Adobe y sus productos son marcas de Adobe Inc. Adobado Kit no está afiliado a Adobe.

## Política de integración

1. Crear un fork propio por app: Adobado Photo, Adobado Vector, Adobado Film, Adobado Sound, Adobado Press, Adobado Light.
2. Fijar el commit upstream y no hacer merge automático. Las actualizaciones se revisan y se prueban.
3. Eliminar de la build las marcas, logos y assets de ArtCraft; sustituirlos por la identidad de Adobado Kit.
4. Conservar LICENSE-MIT, LICENSE-APACHE, NOTICE y ATTRIBUTION.md; añadir ADOBADO.md con el commit de origen y la lista de cambios.
5. Renombrar metadatos, título de ventana, iconos, about y textos de producto.
6. Compilar en Windows y probar abrir, editar y exportar antes de marcar la app como disponible.
7. Documentar el estado real: alpha upstream no es beta nuestra.

## Build de referencia

Requisitos: Rust 1.95 o superior y cargo. En Windows ya hay toolchain instalado.

    cargo run --release -p photocraft -- imagen.psd

El workspace de PhotoCraft es grande (decenas de crates, egui/wgpu, dependencias git). La primera compilación puede tardar varios minutos y no se ha ejecutado todavía en este equipo.

## Estado actual

- Adobado Kit 0.2.0 ya no incluye Markdown Studio ni XLSX Viewer: el hub solo cubre las apps Adobado.
- Ocho repos standalone, no forks: PhotoAdobado, ArtAdobado, FilmAdobado, EffectAdobado, LightAdobado, SoundAdobado, DesignAdobado y PdfAdobado.
- Cada repo conserva licencias y avisos y añade docs/ADOBADO.md con el commit de origen.
- Ninguna build de Windows está validada todavía: el estado es Alpha.
- PdfAdobado puede necesitar un reintento de creación si GitHub aplica su límite temporal de repos.

## Sincronización

El script tools/sync-upstream.sh descarga los repos fijados en upstream/ (ignorado por git) para consulta y diff. No copia código a las apps automáticamente.
