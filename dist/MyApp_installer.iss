[Setup]
AppName=MyApp
AppVersion=1.0
DefaultDirName={autopf}\MyApp
DefaultGroupName=MyApp
OutputDir=dist
OutputBaseFilename=MyApp_Setup
Compression=lzma
SolidCompression=yes
Uninstallable=yes

[Files]
Source: "dist\MyApp.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MyApp"; Filename: "{app}\MyApp.exe"
Name: "{commondesktop}\MyApp"; Filename: "{app}\MyApp.exe"
