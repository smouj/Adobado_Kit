import io
apps = [
 ("SoundAdobado","/home/smouj/adobado-import/SoundAdobado"),
 ("PhotoAdobado","/home/smouj/PhotoAdobado-standalone"),
 ("FilmAdobado","/home/smouj/adobado-import/FilmAdobado"),
]
for app, dest in apps:
    p = dest + "/README.md"
    lines = io.open(p, encoding="utf-8").read().split(chr(10))
    img = None
    out = []
    for line in lines:
        if line.startswith("![") and "docs/screenshot.png" in line and img is None:
            img = line
        else:
            out.append(line)
    if img is None:
        print("NO_IMG", app); continue
    idx = None
    for i,l in enumerate(out):
        if l.startswith("## Estado"):
            idx = i; break
    if idx is None:
        for i,l in enumerate(out):
            if i > 0 and l.startswith("## "):
                idx = i; break
    if idx is None:
        idx = len(out)
    out[idx:idx] = [img, ""]
    io.open(p,"w",encoding="utf-8").write(chr(10).join(out))
    print("moved", app)
