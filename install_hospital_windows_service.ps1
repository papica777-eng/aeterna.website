<#
.SYNOPSIS
    AETERNA-VHT Hospital Edge Server Windows Background Service Installer
.DESCRIPTION
    Installs and registers aeterna_clinical_audit_server.py as a persistent
    Zero-Cloud background Task/Service on port 8890.
    Compliance: EU MDR 2017/745 Class IIb & GDPR Article 9.
#>

param (
    [string]$TaskName = "AETERNA_VHT_Hospital_Edge_8890",
    [string]$ServerPort = "8890"
)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  AETERNA-VHT HOSPITAL EDGE SERVICE REGISTRATION (PORT $ServerPort)" -ForegroundColor Green
Write-Host "  Zero-Cloud Hospital LAN Substrate | Automatic Background Execution" -ForegroundColor DarkCyan
Write-Host "===============================================================================" -ForegroundColor Cyan

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BatchScript = Join-Path $CurrentDir "run_hospital_edge_service.bat"

if (-not (Test-Path $BatchScript)) {
    Write-Error "Could not find run_hospital_edge_service.bat in $CurrentDir"
    exit 1
}

# Register Scheduled Task to run at System Startup with Highest Privileges
$Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$BatchScript`"" -WorkingDirectory $CurrentDir
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1)

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
        Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description "AETERNA-VHT Hospital Edge Clinical Audit & Simulation Daemon on Port $ServerPort" -ErrorAction Stop | Out-Null
        Write-Host "[OK] Successfully registered SYSTEM daemon (Scheduled Task): $TaskName" -ForegroundColor Green
        Write-Host "[OK] Trigger: Automatic on System Startup" -ForegroundColor Green
        Write-Host "[OK] Port: https://127.0.0.1:$ServerPort" -ForegroundColor Green
    } catch {
        Write-Warning "Scheduled task registration error: $_"
    }
} else {
    Write-Warning "Running in non-elevated user mode. Registering autonomous background startup launcher..."
    $StartupFolder = [Environment]::GetFolderPath("Startup")
    $VbsLauncher = Join-Path $CurrentDir "launch_hospital_edge_silent.vbs"
    $VbsContent = "Set WshShell = CreateObject(""WScript.Shell"")" + "`r`n" + "WshShell.Run """"$BatchScript"""", 0, False"
    Set-Content -Path $VbsLauncher -Value $VbsContent -Encoding ASCII
    
    $ShortcutPath = Join-Path $StartupFolder "AETERNA_Hospital_Edge_8890.lnk"
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = "wscript.exe"
    $Shortcut.Arguments = """$VbsLauncher"""
    $Shortcut.WorkingDirectory = $CurrentDir
    $Shortcut.Description = "AETERNA-VHT Hospital Edge Server Background Daemon (Port $ServerPort)"
    $Shortcut.Save()
    
    Write-Host "[OK] Successfully registered persistent user startup launcher (Silent VBS Lnk)" -ForegroundColor Green
    Write-Host "[OK] Path: $ShortcutPath" -ForegroundColor Green
    Write-Host "[OK] Trigger: Automatic on User Login" -ForegroundColor Green
    Write-Host "[OK] Console: Hidden Background Process" -ForegroundColor Green
    Write-Host "[OK] Port: https://127.0.0.1:$ServerPort" -ForegroundColor Green
}

Write-Host "`nTo start the service immediately, execute:" -ForegroundColor Yellow
Write-Host "Start-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor White
