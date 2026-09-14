<#
.SYNOPSIS
    AETERNA-VHT Secure Hospital OTA Pull-Updater Installer (NIS2 & GDPR Art. 9 Compliant)
.DESCRIPTION
    Registers a background Scheduled Task to poll for cryptographically signed updates
    and execute off-hours hot-swaps at 03:00 AM without opening inbound firewall ports.
#>

param (
    [string]$TaskName = "AETERNA_VHT_Hospital_OTA_Updater",
    [string]$ScheduledTime = "03:00"
)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  AETERNA-VHT SECURE HOSPITAL OTA PULL-UPDATER REGISTRATION" -ForegroundColor Green
Write-Host "  Compliance: NIS2 Directive (EU 2022/2555) & GDPR Article 9" -ForegroundColor DarkCyan
Write-Host "===============================================================================" -ForegroundColor Cyan

$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PythonScript = Join-Path $CurrentDir "aeterna_hospital_ota_updater.py"

if (-not (Test-Path $PythonScript)) {
    Write-Error "Could not find aeterna_hospital_ota_updater.py in $CurrentDir"
    exit 1
}

# Resolve python interpreter
$PythonExe = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
if (-not $PythonExe) {
    $PythonExe = "python.exe"
}

# Register Scheduled Task to run daily at 03:00 AM
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$PythonScript`" --force" -WorkingDirectory $CurrentDir
$Trigger = New-ScheduledTaskTrigger -Daily -At $ScheduledTime
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description "AETERNA-VHT Autonomous Pull-Updater (NIS2 Secure Staging & Verification)" | Out-Null
    Write-Host "[OK] Successfully registered persistent hospital OTA task: $TaskName" -ForegroundColor Green
    Write-Host "[OK] Execution Window: Daily at $ScheduledTime AM (Off-hours Hot Swap)" -ForegroundColor Green
    Write-Host "[OK] Inbound Ports Opened: 0 (Zero Inbound Exposure)" -ForegroundColor Green
} catch {
    Write-Warning "Could not register SYSTEM task (requires Administrator privileges). Falling back to CurrentUser task..."
    $PrincipalUser = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $PrincipalUser -Settings $Settings -Description "AETERNA-VHT Autonomous Pull-Updater (User Session)" | Out-Null
    Write-Host "[OK] Successfully registered user OTA task: $TaskName" -ForegroundColor Green
}

Write-Host "`nTo perform an immediate update verification right now, execute:" -ForegroundColor Yellow
Write-Host "python aeterna_hospital_ota_updater.py --force" -ForegroundColor White
