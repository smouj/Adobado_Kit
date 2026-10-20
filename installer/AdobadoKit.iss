[Setup]
AppName=Adobado Kit Launcher
AppVersion=0.3.0
AppPublisher=SMOUJ013
DefaultDirName={autopf}\Adobado Kit
DefaultGroupName=Adobado Kit
OutputDir=output
OutputBaseFilename=AdobadoKit-Setup
SetupIconFile=theme\setup.ico
UninstallDisplayIcon={app}\launcher.ico
WizardStyle=modern
WizardImageFile=theme\wizard.bmp
WizardSmallImageFile=theme\wizard-small.bmp
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
PrivilegesRequired=lowest

[Files]
Source: "launcher\AdobadoLauncher.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "launcher\launcher.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "launcher\launcher.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "launcher\icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs
Source: "theme\*"; DestDir: "{app}\theme"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Adobado Kit"; Filename: "{app}\AdobadoLauncher.exe"; IconFilename: "{app}\launcher.ico"
Name: "{autodesktop}\Adobado Kit"; Filename: "{app}\AdobadoLauncher.exe"; IconFilename: "{app}\launcher.ico"

[Run]
Filename: "{app}\AdobadoLauncher.exe"; Description: "Abrir Adobado Kit"; Flags: nowait postinstall skipifsilent
