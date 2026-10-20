import os, subprocess, shutil, zipfile
APPS = [
 ("ArtAdobado", "39421150554", "/mnt/d/AdobadoApps/ArtDL", "/mnt/d/AdobadoApps/ArtApp"),
 ("LightAdobado", "39421165035", "/mnt/d/AdobadoApps/LightDL", "/mnt/d/AdobadoApps/LightApp"),
 ("EffectAdobado", "39424916230", "/mnt/d/AdobadoApps/EffectDL", "/mnt/d/AdobadoApps/EffectApp"),
 ("DesignAdobado", "39422902838", "/mnt/d/AdobadoApps/DesignDL", "/mnt/d/AdobadoApps/DesignApp"),
]
for app, run, dl, out in APPS:
    shutil.rmtree(dl, ignore_errors=True)
    os.makedirs(dl, exist_ok=True)
    p = subprocess.run(["gh","run","download",run,"--repo","smouj/"+app,"--name",app+"-windows-x64","-D",dl], capture_output=True, text=True)
    zips=[]
    for dp,dn,fns in os.walk(dl):
        for fn in fns:
            if fn.lower().endswith(".zip"):
                zips.append(os.path.join(dp,fn))
    print(app, "rc", p.returncode, "zips", [os.path.basename(z) for z in zips])
    if zips:
        shutil.rmtree(out, ignore_errors=True); os.makedirs(out, exist_ok=True)
        try:
            with zipfile.ZipFile(zips[0]) as z: z.extractall(out)
            exes=[f for f in os.listdir(out) if f.lower().endswith(".exe")]
            print("  exe", exes)
        except Exception as e:
            print("  unzip error", e)
