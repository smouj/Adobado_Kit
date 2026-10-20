from __future__ import annotations
from pathlib import Path
from PIL import Image
import base64, hashlib, re, struct

APPS = {
    'photo': ('PhotoAdobado', 'photocraft', 'PhotoAdobado'),
    'art': ('ArtAdobado', 'vectorcraft', 'ArtAdobado'),
    'film': ('FilmAdobado', 'filmcraft', 'FilmAdobado'),
    'effect': ('EffectAdobado', 'effectcraft', 'EffectAdobado'),
    'light': ('LightAdobado', 'lightcraft', 'LightAdobado'),
    'sound': ('SoundAdobado', 'soundcraft', 'SoundAdobado'),
    'design': ('DesignAdobado', 'designcraft', 'DesignAdobado'),
    'pdf': ('PdfAdobado', 'pdfcraft', 'PdfAdobado'),
}
SIZES=(16,24,32,48,64,128,256,512)

def copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def make_svg(png: Path) -> bytes:
    encoded=base64.b64encode(png.read_bytes()).decode('ascii')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="512" height="512" viewBox="0 0 512 512">\n'
            f'  <image width="512" height="512" xlink:href="data:image/png;base64,{encoded}"/>\n'
            f'</svg>\n').encode('ascii')

def resize_png(src: Path, size: int) -> bytes:
    with Image.open(src) as im:
        im=im.convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
        from io import BytesIO
        out=BytesIO(); im.save(out,format='PNG',optimize=True); return out.getvalue()

def make_icns(src1024: Path, dest: Path):
    chunks=[]
    with Image.open(src1024) as source:
        for size,kind in ((128,b'ic07'),(256,b'ic08'),(512,b'ic09'),(1024,b'ic10')):
            im=source.convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
            from io import BytesIO
            buf=BytesIO(); im.save(buf,format='PNG',optimize=True); png=buf.getvalue()
            chunks.append(kind+struct.pack('>I',8+len(png))+png)
    body=b''.join(chunks)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(b'icns'+struct.pack('>I',8+len(body))+body)

def validate_pack(pack: Path):
    sums={}
    for line in (pack/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        parts=line.strip().split(None,1)
        if len(parts)==2:
            name=parts[1].lstrip('*').replace('\\','/')
            sums[name]=parts[0].lower()
    for rel,want in sums.items():
        path=pack/rel
        if not path.is_file() or sha(path)!=want:
            raise SystemExit(f'Pack hash mismatch: {rel}')
    for slug,(_,_,label) in APPS.items():
        for ext in ('png','ico'):
            rel=f'{"png/1024" if ext=="png" else "ico"}/{label}.{ext}'
            if rel not in sums: raise SystemExit(f'Unlisted official asset: {rel}')
    print(f'Validated {len(sums)} checksums from official icon pack')

def install_kit(pack: Path, kit: Path):
    launcher_label='AdobadoKit_Launcher'
    launcher_png=pack/'png/1024'/f'{launcher_label}.png'
    launcher_ico=pack/'ico'/f'{launcher_label}.ico'
    for dest in (kit/'launcher/launcher.png',kit/'launcher/icons/launcher.png',kit/'assets/icons/launcher.png'):
        copy(launcher_png,dest)
    for dest in (kit/'launcher/launcher.ico',kit/'launcher/icons/launcher.ico',kit/'installer/theme/setup.ico',kit/'installer/theme/uninstall.ico',kit/'assets/icons/launcher.ico'):
        copy(launcher_ico,dest)
    svg=make_svg(pack/'png/512'/f'{launcher_label}.png')
    (kit/'launcher/launcher.svg').write_bytes(svg)
    (kit/'assets/logo.svg').write_bytes(svg)
    for slug,(_,_,label) in APPS.items():
        png=pack/'png/1024'/f'{label}.png'; ico=pack/'ico'/f'{label}.ico'
        copy(png,kit/f'assets/icons/{slug}.png'); copy(ico,kit/f'assets/icons/{slug}.ico')
        copy(png,kit/f'launcher/icons/{slug}.png'); copy(ico,kit/f'launcher/icons/{slug}.ico')
        (kit/f'assets/icons/svg/{slug}.svg').write_bytes(make_svg(pack/'png/512'/f'{label}.png'))
    # A simple, readable family sheet derived only from the eight canonical app marks.
    sheet=Image.new('RGBA',(1120,560),(8,10,14,255))
    for i,(slug,(_,_,label)) in enumerate(APPS.items()):
        with Image.open(pack/'png/256'/f'{label}.png') as im:
            icon=im.convert('RGBA')
        x=24+(i%4)*272; y=24+(i//4)*272
        sheet.alpha_composite(icon,(x,y))
    for dest in (kit/'assets/icons/family.png',kit/'launcher/icons/family.png'):
        dest.parent.mkdir(parents=True,exist_ok=True); sheet.save(dest,format='PNG',optimize=True)
    print('Synchronized Kit and launcher canonical icon sources')

def install_apps(pack: Path, repos_root: Path):
    for slug,(repo,crate,label) in APPS.items():
        root=repos_root/repo; packpng=pack/'png/1024'/f'{label}.png'; png512=pack/'png/512'/f'{label}.png'; ico=pack/'ico'/f'{label}.ico'
        appicon=root/'assets/app-icon'; icon_svg='icon.svg' if slug=='sound' else f'{crate}.svg'
        svg=make_svg(png512)
        (appicon/icon_svg).write_bytes(svg)
        (appicon/f'{crate}-small.svg').write_bytes(svg)
        app_id=f'ai.storyteller.{crate}'
        (appicon/f'hicolor/scalable/apps/{app_id}.svg').write_bytes(svg)
        copy(packpng,appicon/f'{crate}-1024.png')
        copy(png512,appicon/f'{crate}-macos-512.png')
        copy(ico,appicon/f'{crate}.ico')
        make_icns(packpng,appicon/f'{crate}.icns')
        # Replace all pre-existing app icon hicolor raster sizes, and ensure a consistent full set.
        for size in SIZES:
            dest=appicon/f'hicolor/{size}x{size}/apps/{app_id}.png'
            dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(resize_png(packpng,size))
        # The Adobado-facing logo used in product READMEs and the independent brand folder share identical bytes.
        copy(packpng,root/'assets/adobado/icon.png'); copy(ico,root/'assets/adobado/icon.ico')
        for name in ('adobado-logo.png','adobado-logo-white.png'):
            p=root/f'docs/brand/{name}'
            if p.exists(): copy(packpng,p)
        # Ensure the app-icon license covers the user-owned official family; preserve app-code licenses.
        license_text='''Adobado official product icon\n\nThe icon artwork in this directory and assets/adobado is original work by @smouj, supplied in Adobado_Icon_Pack_Final.zip. The copyright holder has authorized redistribution under either the MIT License or the Apache License, Version 2.0, at the recipient’s option.\n\nSee LICENSE-MIT.txt and LICENSE-APACHE.txt in this directory for the complete licence texts. The artwork is not derived from Adobe products.\n'''
        (appicon/'LICENSE.txt').write_text(license_text,encoding='utf-8',newline='\n')
        # Bundle complete license texts beside the icon source.
        for source,name in ((root/'LICENSE-MIT','LICENSE-MIT.txt'),(root/'LICENSE-APACHE','LICENSE-APACHE.txt')):
            if source.exists(): copy(source,appicon/name)
        readme=f'''# {repo} app icon\n\nOfficial Adobado product mark from the owner-supplied `Adobado_Icon_Pack_Final.zip`.\n\nThe PNG and ICO sources are copied byte-for-byte from the pack. The SVG packaging wrappers embed the official 512 px PNG, and the ICNS/hicolor images are size-appropriate renders of the official 1024 px PNG.\n\nAuthor: @smouj (project owner). Source: original work supplied for Adobado Kit; the pack’s `SHA256SUMS.txt` was verified before synchronization. Licence: MIT OR Apache-2.0; complete texts are in `LICENSE-MIT.txt` and `LICENSE-APACHE.txt`.\n'''
        (appicon/'README.md').write_text(readme,encoding='utf-8',newline='\n')
        if repo == 'FilmAdobado':
            copy(pack/'png/256'/f'{label}.png',root/'apps/filmcraft-web/web/favicon.png')
        if repo == 'EffectAdobado':
            (root/'apps/effectcraft-web/web/favicon.svg').write_bytes(svg)
        print('Synchronized',repo)

def main() -> int:
    import argparse
    parser=argparse.ArgumentParser(description="Synchronize the owner-supplied official Adobado icon family.")
    parser.add_argument("--pack-dir",type=Path,required=True,help="Extracted Adobado_Icon_Pack_Final directory")
    parser.add_argument("--kit-root",type=Path,default=Path(__file__).resolve().parents[1],help="Adobado_Kit repository root")
    parser.add_argument("--app-repos-root",type=Path,help="Directory containing the eight app repositories")
    parser.add_argument("--apply",action="store_true",help="Write the synchronized official icons")
    args=parser.parse_args()
    if not args.apply:
        parser.error("pass --apply to write files; without it this tool does not modify repositories")
    pack=args.pack_dir.resolve(); kit=args.kit_root.resolve()
    validate_pack(pack)
    install_kit(pack,kit)
    if args.app_repos_root:
        install_apps(pack,args.app_repos_root.resolve())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
