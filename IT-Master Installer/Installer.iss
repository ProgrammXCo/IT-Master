; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "IT Master"
#define MyAppVersion "3.5.2 (pre-build)"
#define MyAppPublisher "ProgrammX"
#define MyAppURL "https://github.com/ProgrammXCo"
#define MyAppExeName "IT Master.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{FA4694F1-4AFC-4853-BCB4-CE5ADCB3902F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=C:\MyScripts\Python\Projects\IT-Master\IT Master Installer
OutputBaseFilename=IT Master Installer
SetupIconFile=C:\MyScripts\Python\Projects\IT-Master\IT Master Installer\installer icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
Name: "{app}"; Permissions: users-full

[Files]
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\courses\*"; DestDir: "{app}\courses"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\PIL\*"; DestDir: "{app}\PIL"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\PyQt6\*"; DestDir: "{app}\PyQt6"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_elementtree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_queue.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_sqlite3.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\base_library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\libcrypto-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\libffi-8.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\libssl-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\LOG.log"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\python3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\python311.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\settings.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\sqlite3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\MyScripts\Python\Projects\IT-Master\dist\IT Master\VCRUNTIME140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

