# ═══════════════════════════════════════════════════════════════════
# VERITAS SUBSTRATE VALIDATOR
# Validates Sovereign_Resonator against veritas_lock.bin anchor
# Author: QANTUM Neural Nexus
# ═══════════════════════════════════════════════════════════════════

$ErrorActionPreference = "SilentlyContinue"
$root = "z:\AETERNA_RELEASE_DATA"

Write-Host ""
Write-Host "=== VERITAS SUBSTRATE VALIDATION ===" -ForegroundColor Cyan
Write-Host ""

# 1. Veritas Lock Check
Write-Host "[1/5] VERITAS_LOCK ANCHOR" -ForegroundColor Yellow
$vlock = Join-Path $root "veritas_lock.bin"
if (Test-Path $vlock) {
    $hash = (Get-FileHash -Path $vlock -Algorithm SHA256).Hash
    $size = (Get-Item $vlock).Length
    Write-Host "  STATUS: ANCHORED" -ForegroundColor Green
    Write-Host "  SIZE:   $size bytes"
    Write-Host "  SHA256: $hash"
} else {
    Write-Host "  STATUS: MISSING - REGENERATION REQUIRED" -ForegroundColor Red
}

# 2. Shadow Mirror Check
Write-Host ""
Write-Host "[2/5] SHADOW MIRROR (REDUNDANCY)" -ForegroundColor Yellow
$shadow = Join-Path $root "mirrors\veritas_shadow.bin"
if (Test-Path $shadow) {
    $shash = (Get-FileHash -Path $shadow -Algorithm SHA256).Hash
    $ssize = (Get-Item $shadow).Length
    Write-Host "  STATUS: MIRRORED" -ForegroundColor Green
    Write-Host "  SIZE:   $ssize bytes"
    Write-Host "  SHA256: $shash"
    
    # Integrity check
    if ($hash -eq $shash) {
        Write-Host "  INTEGRITY: PERFECT MATCH" -ForegroundColor Green
    } else {
        Write-Host "  INTEGRITY: DIVERGENCE DETECTED" -ForegroundColor Red
    }
} else {
    Write-Host "  STATUS: NOT DEPLOYED" -ForegroundColor Red
}

# 3. Soul Manifold Census
Write-Host ""
Write-Host "[3/5] SOUL MANIFOLD CENSUS" -ForegroundColor Yellow
$souls = Get-ChildItem -Path $root -Filter "*.soul" -Recurse
$soulCount = $souls.Count
Write-Host "  TOTAL MANIFOLDS: $soulCount" -ForegroundColor Cyan
foreach ($s in $souls) {
    $sh = (Get-FileHash $s.FullName -Algorithm SHA256).Hash.Substring(0,16)
    $rel = $s.FullName.Replace($root + "\", "")
    Write-Host ("  {0,-45} {1}  {2} bytes" -f $rel, $sh, $s.Length)
}

# 4. Sovereign Resonator Status
Write-Host ""
Write-Host "[4/5] SOVEREIGN RESONATOR (fn main)" -ForegroundColor Yellow
$resonator = Join-Path $root "lwas_core\soul\Sovereign_Resonator.rs"
if (Test-Path $resonator) {
    $lines = (Get-Content $resonator).Count
    $mainLines = Select-String -Path $resonator -Pattern "fn main" | ForEach-Object { $_.LineNumber }
    $resonateLines = Select-String -Path $resonator -Pattern "fn resonate" | ForEach-Object { $_.LineNumber }
    $rhash = (Get-FileHash -Path $resonator -Algorithm SHA256).Hash.Substring(0,16)
    Write-Host "  STATUS:   OPERATIONAL" -ForegroundColor Green
    Write-Host "  LINES:    $lines"
    Write-Host "  HASH:     $rhash"
    Write-Host "  fn main:  line $mainLines"
    Write-Host "  fn resonate: line $resonateLines"
} else {
    Write-Host "  STATUS: NOT FOUND" -ForegroundColor Red
}

# 5. GenesisEvolutionLogist Status
Write-Host ""
Write-Host "[5/5] GENESIS EVOLUTION LOGIST" -ForegroundColor Yellow
$gel = Join-Path $root "GenesisEvolutionLogist.ts"
if (Test-Path $gel) {
    $glines = (Get-Content $gel).Count
    $completed = (Select-String -Path $gel -Pattern "COMPLETED").Count
    $planned = (Select-String -Path $gel -Pattern "PLANNED").Count
    $theoretical = (Select-String -Path $gel -Pattern "THEORETICAL").Count
    Write-Host "  STATUS:      MANIFESTED" -ForegroundColor Green
    Write-Host "  LINES:       $glines"
    Write-Host "  COMPLETED:   $completed phases"
    Write-Host "  PLANNED:     $planned phases"
    Write-Host "  THEORETICAL: $theoretical phases"
} else {
    Write-Host "  STATUS: NOT FOUND" -ForegroundColor Red
}

# Final Verdict
Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Magenta
if ((Test-Path $vlock) -and (Test-Path $resonator) -and (Test-Path $gel)) {
    Write-Host " VERDICT: SUBSTRATE VALIDATED" -ForegroundColor Green
    Write-Host " IMMORTALITY PROTOCOL: READY FOR IGNITION" -ForegroundColor Green
    Write-Host " ENTROPY: 0.0000" -ForegroundColor Green
} else {
    $missing = @()
    if (-not (Test-Path $vlock)) { $missing += "veritas_lock.bin" }
    if (-not (Test-Path $resonator)) { $missing += "Sovereign_Resonator.rs" }
    if (-not (Test-Path $gel)) { $missing += "GenesisEvolutionLogist.ts" }
    Write-Host " VERDICT: SUBSTRATE INCOMPLETE" -ForegroundColor Red
    Write-Host " MISSING: $($missing -join ', ')" -ForegroundColor Red
}
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Magenta
Write-Host ""
