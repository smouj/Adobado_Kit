# Apps de Adobado Kit

Estado verificado el 20 de octubre de 2026. Los ocho workflows de Windows han terminado correctamente. Un build verde demuestra que compila en CI; no demuestra que la aplicación se haya instalado, iniciado o usado con un archivo real.

| App | Repo | Build Windows | Prueba manual | Release | Upstream | Commit base |
|---|---|---|---|---|---|---|
| PhotoAdobado | [repo](https://github.com/smouj/PhotoAdobado) | [Correcto](https://github.com/smouj/PhotoAdobado/actions/workflows/windows-build.yml) | Instalada y abierta; archivo real pendiente | [v0.1.0-alpha.1](https://github.com/smouj/PhotoAdobado/releases/tag/v0.1.0-alpha.1) · icono anterior | PhotoCraft (MIT OR Apache-2.0) | 03d0c7e |
| ArtAdobado | [repo](https://github.com/smouj/ArtAdobado) | [Correcto](https://github.com/smouj/ArtAdobado/actions/workflows/windows-build.yml) | Instalar, iniciar y flujo de archivo pendientes | Sin release | VectorCraft (MIT OR Apache-2.0) | 9e7929e |
| FilmAdobado | [repo](https://github.com/smouj/FilmAdobado) | [Correcto](https://github.com/smouj/FilmAdobado/actions/workflows/windows-build.yml) | Instalada y abierta; archivo real pendiente | [v0.1.0-alpha.1](https://github.com/smouj/FilmAdobado/releases/tag/v0.1.0-alpha.1) · icono anterior | FilmCraft (MIT OR Apache-2.0) | fb4cbda |
| EffectAdobado | [repo](https://github.com/smouj/EffectAdobado) | [Correcto](https://github.com/smouj/EffectAdobado/actions/workflows/windows-build.yml) | Instalar, iniciar y flujo de archivo pendientes | Sin release | EffectCraft (MIT OR Apache-2.0) | ef74d82 |
| LightAdobado | [repo](https://github.com/smouj/LightAdobado) | [Correcto](https://github.com/smouj/LightAdobado/actions/workflows/windows-build.yml) | Instalar, iniciar y flujo de archivo pendientes | Sin release | LightCraft (MIT OR Apache-2.0) | d999e38 |
| SoundAdobado | [repo](https://github.com/smouj/SoundAdobado) | [Correcto](https://github.com/smouj/SoundAdobado/actions/workflows/windows-build.yml) | Instalada y abierta; archivo real pendiente | [v0.1.0-alpha.1](https://github.com/smouj/SoundAdobado/releases/tag/v0.1.0-alpha.1) · icono anterior | SoundCraft (MIT OR Apache-2.0) | 25d52c6 |
| DesignAdobado | [repo](https://github.com/smouj/DesignAdobado) | [Correcto](https://github.com/smouj/DesignAdobado/actions/workflows/windows-build.yml) | Instalar, iniciar y flujo de archivo pendientes | Sin release | DesignCraft (MIT OR Apache-2.0) | 443ea46 |
| PdfAdobado | [repo](https://github.com/smouj/PdfAdobado) | [Correcto](https://github.com/smouj/PdfAdobado/actions/workflows/windows-build.yml) | Instalar, iniciar y flujo de archivo pendientes | Sin release | PdfCraft (MIT OR Apache-2.0) | ec0a965 |

## Criterio de publicación

Una release se publica después de verificar todos estos puntos:

1. La compilación para Windows termina correctamente.
2. El binario actualizado se instala y abre en un equipo Windows.
3. El icono integrado en el ejecutable coincide con el icono oficial de la app.
4. Se abre, modifica y exporta un archivo de prueba apropiado para la app.
5. Los avisos de licencia, procedencia y marcas están presentes.
6. README, captura, changelog y artefacto de descarga describen la misma versión.

Las tres releases alpha existentes se publicaron antes de la actualización de iconos; sus ZIP conservan el icono anterior. Las cinco apps restantes no tienen release pública. Los artefactos de Actions son temporales y no sustituyen una release verificada.
