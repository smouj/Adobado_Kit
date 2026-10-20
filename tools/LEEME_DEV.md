# Adobado Kit — desarrollo local

Cada app es un repo independiente. Aquí tienes acceso directo a su código y a las instrucciones para modificarlo.

## Repos

- PhotoAdobado: https://github.com/smouj/PhotoAdobado — paquete photocraft
- ArtAdobado: https://github.com/smouj/ArtAdobado — paquete vectorcraft
- FilmAdobado: https://github.com/smouj/FilmAdobado — paquete filmcraft
- EffectAdobado: https://github.com/smouj/EffectAdobado — paquete effectcraft
- LightAdobado: https://github.com/smouj/LightAdobado — paquete lightcraft
- SoundAdobado: https://github.com/smouj/SoundAdobado — paquete soundcraft
- DesignAdobado: https://github.com/smouj/DesignAdobado — paquete designcraft
- PdfAdobado: https://github.com/smouj/PdfAdobado — paquete pdfcraft

## Copias locales

Las copias de trabajo están en WSL:

- /home/smouj/PhotoAdobado-standalone
- /home/smouj/adobado-import/ArtAdobado
- /home/smouj/adobado-import/FilmAdobado
- /home/smouj/adobado-import/EffectAdobado
- /home/smouj/adobado-import/LightAdobado
- /home/smouj/adobado-import/SoundAdobado
- /home/smouj/adobado-import/DesignAdobado
- /home/smouj/adobado-import/PdfAdobado

## Build en Windows

Requisitos: Rust 1.95+, CMake y NASM.

    cargo build --release -p <paquete>

El ejecutable sale en target/release. El CI de cada repo compila en windows-latest y publica un artifact.

## Estado

- Instaladas y probadas: PhotoAdobado, FilmAdobado, SoundAdobado.
- Build OK, artifact pendiente de descarga: ArtAdobado, LightAdobado, EffectAdobado, DesignAdobado.
- PdfAdobado: build en curso.

Hub: https://github.com/smouj/Adobado_Kit
