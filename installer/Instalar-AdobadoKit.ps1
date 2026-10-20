$ErrorActionPreference = "Stop"
$src = $PSScriptRoot
$dest = Join-Path $env:LOCALAPPDATA "AdobadoKit"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item (Join-Path $src "launcher\*") $dest -Recurse -Force
$ws = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = $ws.CreateShortcut((Join-Path $desktop "Adobado Kit.lnk"))
$lnk.TargetPath = Join-Path $dest "AdobadoLauncher.exe"
$lnk.WorkingDirectory = $dest
$lnk.IconLocation = (Join-Path $dest "launcher.ico") + ",0"
$lnk.Description = "Adobado Kit Launcher"
$lnk.Save()
$start = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
New-Item -ItemType Directory -Force $start | Out-Null
$lnk2 = $ws.CreateShortcut((Join-Path $start "Adobado Kit.lnk"))
$lnk2.TargetPath = Join-Path $dest "AdobadoLauncher.exe"
$lnk2.WorkingDirectory = $dest
$lnk2.IconLocation = (Join-Path $dest "launcher.ico") + ",0"
$lnk2.Save()
Write-Host "Adobado Kit instalado en $dest"
Write-Host "Acceso directo creado en el escritorio y en el menu Inicio."
