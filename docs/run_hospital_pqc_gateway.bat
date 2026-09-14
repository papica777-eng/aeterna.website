@echo off
REM ==============================================================================
REM === AETERNA QUANTUM NEXUS • HOSPITAL PQC HYBRID GATEWAY LAUNCHER           ===
REM === Protects Hospital Port 8890 with NIST FIPS 203 (ML-KEM-768) Hybrid PQC ===
REM === Compliance: NIS2 Directive Art. 21 §2(h) • Neutralizes SNDL Harvesting ===
REM ==============================================================================

SETLOCAL EnableDelayedExpansion

set PQC_BIN=Z:\AETERNA-PQC-MIGRATION-SUITE\target\debug\aeterna-pqc-gateway.exe
set LISTEN_ADDR=127.0.0.1:8443
set UPSTREAM_ADDR=127.0.0.1:8890

echo ===============================================================================
echo   AETERNA QUANTUM NEXUS: POST-QUANTUM PERIMETER GATEWAY
echo   Hybrid KEM: X25519 + ML-KEM-768 (NIST FIPS 203)
echo   Listening on: %LISTEN_ADDR% -^> Forwarding to Edge Engine: %UPSTREAM_ADDR%
echo ===============================================================================

if not exist "%PQC_BIN%" (
    echo [ERROR] PQC Gateway binary not found at %PQC_BIN%
    echo Building AETERNA Quantum Nexus binary...
    pushd Z:\AETERNA-PQC-MIGRATION-SUITE
    cargo build --bin aeterna-pqc-gateway
    popd
)

"%PQC_BIN%" --listen %LISTEN_ADDR% --upstream %UPSTREAM_ADDR% --hybrid-pqc
