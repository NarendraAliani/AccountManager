$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$desktop = [Environment]::GetFolderPath("Desktop")
$wsh = New-Object -ComObject WScript.Shell
$icon = Join-Path $root "static\favicon.ico"

function New-Shortcut {
    param(
        [string]$Name,
        [string]$TargetPath,
        [string]$Arguments = "",
        [string]$WorkingDirectory = $root,
        [string]$IconLocation = $icon
    )

    $shortcutPath = Join-Path $desktop $Name
    $shortcut = $wsh.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $TargetPath
    $shortcut.Arguments = $Arguments
    $shortcut.WorkingDirectory = $WorkingDirectory
    if (Test-Path $IconLocation) {
        $shortcut.IconLocation = $IconLocation
    }
    $shortcut.Save()
    Write-Host "Created shortcut: $shortcutPath"
}

New-Shortcut -Name "AccountManager - Start Setup.lnk" -TargetPath (Join-Path $root "Start Setup.bat")
New-Shortcut -Name "AccountManager - Launch App.lnk" -TargetPath (Join-Path $root "launch_local.bat")

Write-Host ""
Write-Host "Desktop shortcuts were created successfully."
