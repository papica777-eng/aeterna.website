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

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description "AETERNA-VHT Hospital Edge Clinical Audit & Simulation Daemon on Port $ServerPort" | Out-Null
    Write-Host "[OK] Successfully registered persistent hospital edge daemon: $TaskName" -ForegroundColor Green
    Write-Host "[OK] Trigger: Automatic on System Startup" -ForegroundColor Green
    Write-Host "[OK] Port: https://127.0.0.1:$ServerPort" -ForegroundColor Green
} catch {
    Write-Warning "Could not register SYSTEM task (requires Administrator privileges). Falling back to CurrentUser Logon trigger..."
    $TriggerLogon = New-ScheduledTaskTrigger -AtLogOn
    $PrincipalUser = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $TriggerLogon -Principal $PrincipalUser -Settings $Settings -Description "AETERNA-VHT Hospital Edge Clinical Daemon (User Session)" | Out-Null
    Write-Host "[OK] Successfully registered user startup task: $TaskName" -ForegroundColor Green
}

Write-Host "`nTo start the service immediately, execute:" -ForegroundColor Yellow
Write-Host "Start-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor White
