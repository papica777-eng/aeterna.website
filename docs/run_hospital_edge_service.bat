@echo off
TITLE AETERNA-VHT Hospital Edge Server [Port 8890]
COLOR 0A
cls
echo ===============================================================================
echo   AETERNA-VHT: HOSPITAL EDGE SERVER & AUDIT TRAIL SUBSTRATE (PORT 8890)
echo   On-Premise Hospital LAN Substrate ^| Zero-Cloud (GDPR Article 9)
echo   Compliance: EU AI Act Articles 12 ^& 14 ^| IEC 62304 Class C ^| MDR Class IIb
echo ===============================================================================
echo.

cd /d "%~dp0"

:: 1. Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in system PATH.
    echo Please install Python 3.10+ or add it to PATH.
    pause
    exit /b 1
)

:: 2. Ensure TLS Certificates Exist
if not exist "hospital_edge_cert.pem" (
    echo [*] Generating TLS 1.3 Hospital Self-Signed Certificate...
    if exist "generate_hospital_ssl.py" (
        python generate_hospital_ssl.py
    ) else if exist "c:\Users\papic\AETERNA-PLATFORM\OMNI-VIVISECTOR\soul\BRUTAL_MODULES\aeterna_selye_engine\generate_hospital_ssl.py" (
        python "c:\Users\papic\AETERNA-PLATFORM\OMNI-VIVISECTOR\soul\BRUTAL_MODULES\aeterna_selye_engine\generate_hospital_ssl.py"
    )
)

:: 3. Launching Server Watchdog Daemon
echo [*] Starting AETERNA Hospital Edge Server on https://127.0.0.1:8890 ...
echo [*] Press CTRL+C to stop the service.
echo.

:WATCHDOG_LOOP
if exist "aeterna_clinical_audit_server.py" (
    python aeterna_clinical_audit_server.py
) else if exist "c:\Users\papic\AETERNA-PLATFORM\OMNI-VIVISECTOR\soul\BRUTAL_MODULES\aeterna_selye_engine\aeterna_clinical_audit_server.py" (
    python "c:\Users\papic\AETERNA-PLATFORM\OMNI-VIVISECTOR\soul\BRUTAL_MODULES\aeterna_selye_engine\aeterna_clinical_audit_server.py"
) else (
    echo [ERROR] aeterna_clinical_audit_server.py not found.
    pause
    exit /b 1
)

echo.
echo [!] Server exited or crashed. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto WATCHDOG_LOOP
