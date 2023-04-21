#define MyAppName "WikiSearch"
#define MyAppVersion "1.4.0"
#define MyAppPublisher "Tecwindow"
#define MyAppURL "https://tecwindow.net/"
#define MyAppExeName "WikiSearch.exe"

[Setup]
AppName={#myAppName}
AppVersion={#MyAppVersion}
VersionInfoDescription=WikiSearch setup
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany=tecwindow
VersionInfoCopyright=copyright, ©2022; tecwindow
VersionInfoProductName=WikiSearch
VersionInfoProductVersion={#MyAppVersion}
VersionInfoOriginalFileName=WikiSearch_Setup.exe
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppId={{F3679719-7471-4B3A-A60D-A9BF0B44E7B3}

DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=admin
OutputDir=WikiSearch
OutputBaseFilename=WikiSearchSetup
Compression=lzma
CloseApplications=force
restartApplications=yes
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "WikiSearch\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "WikiSearch\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[CustomMessages]
arabic.AppLNGfile = Arabic
english.AppLNGfile = English
french.AppLNGfile = French
spanish.AppLNGfile = Spanish

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon


[INI]
Filename: "{userappdata}\WikiSearch\Settingss.ini"; Section: "default"; Key: "language"; String: "{cm:AppLNGfile}"
Filename: "{app}\User Data\Settingss.ini"; Section: "default"; Key: "language"; String: "{cm:AppLNGfile}"

[InstallDelete]
Type: filesandordirs; Name: "{app}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall

