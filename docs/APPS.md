# Apps de Adobado Kit

Actualizado el 21 de octubre de 2026. Los ocho builds de Windows terminaron correctamente; sus binarios se instalaron y abrieron en este equipo. Falta validar cada flujo con un archivo real, por lo que el estado confirmado se limita al arranque.

| App | Repositorio | Compilación de Windows | Estado de uso | Descarga pública | Proyecto base | Commit base |
|---|---|---|---|---|---|---|
| PhotoAdobado | [repo](https://github.com/smouj/PhotoAdobado) | [Correcta](https://github.com/smouj/PhotoAdobado/actions/runs/39512138690) | Instalada y abierta en este equipo; archivo real pendiente | [v0.1.0-alpha.1](https://github.com/smouj/PhotoAdobado/releases/tag/v0.1.0-alpha.1) · ZIP alpha con icono anterior | PhotoCraft (MIT OR Apache-2.0) | 03d0c7e |
| ArtAdobado | [repo](https://github.com/smouj/ArtAdobado) | [Correcta](https://github.com/smouj/ArtAdobado/actions/runs/39512141938) | Instalada y abierta en este equipo; archivo real pendiente | Sin paquete público | VectorCraft (MIT OR Apache-2.0) | 9e7929e |
| FilmAdobado | [repo](https://github.com/smouj/FilmAdobado) | [Correcta](https://github.com/smouj/FilmAdobado/actions/runs/39512145200) | Instalada y abierta en este equipo; archivo real pendiente | [v0.1.0-alpha.1](https://github.com/smouj/FilmAdobado/releases/tag/v0.1.0-alpha.1) · ZIP alpha con icono anterior | FilmCraft (MIT OR Apache-2.0) | fb4cbda |
| EffectAdobado | [repo](https://github.com/smouj/EffectAdobado) | [Correcta](https://github.com/smouj/EffectAdobado/actions/runs/39512148138) | Instalada y abierta en este equipo; archivo real pendiente | Sin paquete público | EffectCraft (MIT OR Apache-2.0) | ef74d82 |
| LightAdobado | [repo](https://github.com/smouj/LightAdobado) | [Correcta](https://github.com/smouj/LightAdobado/actions/runs/39512150946) | Instalada y abierta en este equipo; archivo real pendiente | Sin paquete público | LightCraft (MIT OR Apache-2.0) | d999e38 |
| SoundAdobado | [repo](https://github.com/smouj/SoundAdobado) | [Correcta](https://github.com/smouj/SoundAdobado/actions/runs/39512154210) | Instalada y abierta en este equipo; archivo real pendiente | [v0.1.0-alpha.1](https://github.com/smouj/SoundAdobado/releases/tag/v0.1.0-alpha.1) · ZIP alpha con icono anterior | SoundCraft (MIT OR Apache-2.0) | 25d52c6 |
| DesignAdobado | [repo](https://github.com/smouj/DesignAdobado) | [Correcta](https://github.com/smouj/DesignAdobado/actions/runs/39512157800) | Instalada y abierta en este equipo; archivo real pendiente | Sin paquete público | DesignCraft (MIT OR Apache-2.0) | 443ea46 |
| PdfAdobado | [repo](https://github.com/smouj/PdfAdobado) | [Correcta](https://github.com/smouj/PdfAdobado/actions/runs/39512112307) | Instalada y abierta en este equipo; archivo real pendiente | Sin paquete público | PdfCraft (MIT OR Apache-2.0) | ec0a965 |

## Criterio de publicación

Una release se publica después de verificar todos estos puntos:

1. La compilación para Windows termina correctamente.
2. El binario actualizado se instala y abre en un equipo Windows.
3. El icono integrado en el ejecutable coincide con el icono oficial de la app.
4. Se abre, modifica y exporta un archivo de prueba apropiado para la app.
5. Los avisos de licencia, procedencia y marcas están presentes.
6. README, captura, changelog y artefacto de descarga describen la misma versión.

Las tres releases alpha existentes se publicaron antes de la actualización de iconos; sus ZIP conservan el icono anterior. Las cinco apps restantes no tienen release pública. Los artefactos de Actions son temporales y no sustituyen una release verificada.
