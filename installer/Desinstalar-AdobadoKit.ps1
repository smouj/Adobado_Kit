$dest = Join-Path $env:LOCALAPPDATA "AdobadoKit"
$desktop = [Environment]::GetFolderPath("Desktop")
$start = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
Remove-Item (Join-Path $desktop "Adobado Kit.lnk") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $start "Adobado Kit.lnk") -Force -ErrorAction SilentlyContinue
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
Write-Host "Adobado Kit desinstalado."
