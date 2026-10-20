# Adobado Kit

Adobado Kit reúne el catálogo de las ocho aplicaciones y el launcher de Windows. Cada aplicación conserva su propio repositorio, historial, licencia base y estado de compilación.

## Elegir y abrir una aplicación

Consulta el catálogo de [apps y su estado](APPS.md) antes de descargar. El launcher muestra si encuentra el ejecutable en este equipo: **Abrir** inicia una app instalada y **Ver descargas** lleva a las publicaciones de su repositorio.

La versión local del launcher es 0.4.0. La descarga pública enlazada en el README sigue siendo v0.3.2; no se debe presentar una compilación local como release publicada.

## Identidad visual

Los iconos canónicos están en [`assets/icons/`](../assets/icons/). El launcher usa la marca del Kit; cada aplicación usa su icono de producto correspondiente. La paridad entre el catálogo, el launcher y los repositorios de apps se comprueba con:

```powershell
python tools/check_brand_assets.py --app-repos-root "C:\ruta\al\directorio\de\repos"
```

Sustituye la ruta de ejemplo por la carpeta que contiene los ocho clones locales.

Los derechos y atribución del pack están en [`assets/icons/ATTRIBUTION.md`](../assets/icons/ATTRIBUTION.md); los fondos de marca no sustituyen capturas de una interfaz real.

## Antes de publicar

El criterio de release está en [APPS.md](APPS.md): compilar para Windows, instalar y abrir el binario, confirmar el icono integrado y probar una tarea completa con un archivo de muestra apropiado. Mantén separados el estado del código, la instalación local, la prueba funcional y la disponibilidad de una descarga pública.
