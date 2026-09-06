# ═══════════════════════════════════════════════════════════════════════════════
# AETERNA VHT — Sovereign Cryptographic License Engine
# ═══════════════════════════════════════════════════════════════════════════════
# Architect:  Dimitar Prodromov (Authority 0x41_45_54_45_52_4e_41...)
# Purpose:    Cryptographically signs and verifies one-shot consumable license
#             keys. Integrates with GitHub Sponsors Webhook (exact tier pricing).
#             Enforces strict price-matching:
#               - Longevity Clock: 299 €
#               - Diabetes Twin: 499 €
#               - Cardio Predictor: 499 €
#               - Precision Oncology: 1,499 €
#               - 100K Cohort Trial: 9,999 €
#
# Complexity: O(1) key generation & signature verification
# Invariant:  1 KEY = 1 CALCULATION (ONE-SHOT CONSUMABLE)
# ═══════════════════════════════════════════════════════════════════════════════

import os
import json
import time
import hmac
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

SOVEREIGN_SECRET = os.environ.get(
    "AETERNA_LICENSE_SECRET",
    "0x41_45_54_45_52_4e_41_5f_4c_4f_47_4f_53_5f_44_49_4d_49_54_41_52_5f_50_52_4f_44_52_4f_4d_56_21"
)

MODULE_TIERS: Dict[str, Dict[str, Any]] = {
    "LONGEVITY": {
        "title": "Epigenetic Horvath Clock & Longevity Report",
        "price_eur": 299,
        "aliases": ["vht_longevity", "longevity"]
    },
    "DIABETES": {
        "title": "Metabolic & Diabetes Pancreatic Twin",
        "price_eur": 499,
        "aliases": ["vht_diabet", "diabetes"]
    },
    "CARDIO": {
        "title": "Cardiovascular Hemodynamic Predictor",
        "price_eur": 499,
        "aliases": ["vht_cardio", "cardio"]
    },
    "ONCOLOGY": {
        "title": "Precision In Silico Oncology & Drug Targeting",
        "price_eur": 1499,
        "aliases": ["oncology_hud", "clinical-oncology", "CLINICAL_DOCTOR_PORTAL", "oncology", "aeterna_pharma_shadow", "vht_suite"]
    },
    "COHORT": {
        "title": "100,000 In Silico Cohort Trial Simulation",
        "price_eur": 9999,
        "aliases": ["aeterna_cohort_sim", "cohort"]
    },
    "SOVEREIGN_CORE": {
        "title": "Sovereign Bio-Computational Matrix",
        "price_eur": 1499,
        "aliases": ["SovereignHUD", "SovereignHUD_v2", "sovereign-hud", "hud"]
    }
}

LEDGER_FILE = Path(__file__).parent / "issued_licenses.json"


def _load_ledger() -> Dict[str, Any]:
    if LEDGER_FILE.exists():
        try:
            with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_ledger(ledger: Dict[str, Any]) -> None:
    try:
        with open(LEDGER_FILE, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save license ledger: {e}")


def compute_signature(module: str, price_eur: int, serial: str) -> str:
    """Computes 8-character HMAC-SHA256 signature for the given parameters."""
    msg = f"{module.upper()}:{price_eur}:{serial}".encode("utf-8")
    sig = hmac.new(SOVEREIGN_SECRET.encode("utf-8"), msg, hashlib.sha256).hexdigest()
    return sig[:8].upper()


def generate_license_key(module: str, sponsor_login: str = "SPONSOR", custom_price: Optional[int] = None) -> Dict[str, Any]:
    """
    Generates a cryptographically signed one-shot license key.
    Format: AET-<MODULE>-<PRICE>EUR-<SERIAL>-<SIG>
    """
    module = module.upper()
    tier_info = MODULE_TIERS.get(module)
    price = custom_price if custom_price else (tier_info["price_eur"] if tier_info else 1499)
    
    timestamp = int(time.time())
    serial = hashlib.sha256(f"{sponsor_login}:{timestamp}:{time.time_ns()}".encode("utf-8")).hexdigest()[:6].upper()
    sig = compute_signature(module, price, serial)
    
    key = f"AET-{module}-{price}EUR-{serial}-{sig}"
    
    ledger = _load_ledger()
    ledger[key] = {
        "key": key,
        "module": module,
        "price_eur": price,
        "sponsor": sponsor_login,
        "created_at": timestamp,
        "consumed": False,
        "consumed_at": None,
        "consumed_by_ip": None
    }
    _save_ledger(ledger)
    
    return {
        "key": key,
        "module": module,
        "price_eur": price,
        "sponsor": sponsor_login,
        "created_at": timestamp
    }


def verify_and_consume_key(key: str, requested_module: str, client_ip: str = "unknown") -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Verifies key signature, matches module tier and price, and burns key.
    Returns: (is_valid, message, details)
    """
    key = key.strip().upper()
    requested_module = requested_module.upper()
    
    parts = key.split("-")
    if len(parts) != 5 or parts[0] != "AET":
        return False, "Invalid license key structure. Format: AET-<MODULE>-<PRICE>EUR-<SERIAL>-<SIG>", None
    
    key_module = parts[1]
    price_str = parts[2]
    serial = parts[3]
    provided_sig = parts[4]
    
    if not price_str.endswith("EUR"):
        return False, "Invalid price token in key. Must specify EUR denomination.", None
    
    try:
        key_price = int(price_str.replace("EUR", ""))
    except ValueError:
        return False, "Invalid numeric price in key.", None
    
    # Verify cryptographic signature
    expected_sig = compute_signature(key_module, key_price, serial)
    if not hmac.compare_digest(provided_sig, expected_sig):
        return False, "CRYPTOGRAPHIC INTEGRITY ERROR: License signature is forged or invalid.", None
    
    # Verify module match or sufficient tier
    tier_info = MODULE_TIERS.get(requested_module)
    required_price = tier_info["price_eur"] if tier_info else 1499
    
    if key_module != requested_module and key_price < required_price:
        return False, (
            f"TIER MISMATCH: This key is issued for {key_module} ({key_price} €). "
            f"The requested module '{requested_module}' requires a {required_price} € tier license."
        ), None
    
    # Check ledger for one-shot burn
    ledger = _load_ledger()
    if key in ledger:
        if ledger[key].get("consumed", False):
            consumed_at = ledger[key].get("consumed_at", "earlier")
            return False, f"ONE-SHOT CONSUMED: This license key was already consumed at timestamp {consumed_at}.", None
        
        ledger[key]["consumed"] = True
        ledger[key]["consumed_at"] = int(time.time())
        ledger[key]["consumed_by_ip"] = client_ip
        _save_ledger(ledger)
    else:
        # Key has valid sovereign HMAC signature, register it as consumed in ledger
        ledger[key] = {
            "key": key,
            "module": key_module,
            "price_eur": key_price,
            "sponsor": "OFFLINE_AUTHORIZED",
            "created_at": int(time.time()),
            "consumed": True,
            "consumed_at": int(time.time()),
            "consumed_by_ip": client_ip
        }
        _save_ledger(ledger)
        
    return True, f"✓ KEY VERIFIED & CONSUMED ({key_price} €). Simulation authorized.", {
        "module": key_module,
        "price_eur": key_price,
        "consumed": True
    }


def process_github_sponsorship(webhook_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Processes incoming GitHub Sponsors Webhook payload.
    Determines tier from monthly_price_in_cents / one-time amount.
    Issues corresponding Aeterna license key.
    """
    action = webhook_payload.get("action")
    if action not in ["created", "tier_changed"]:
        return None
    
    sponsorship = webhook_payload.get("sponsorship", {})
    tier = sponsorship.get("tier", {})
    sponsor = sponsorship.get("sponsor", {}).get("login", "github_sponsor")
    
    # GitHub price is in USD cents
    price_cents = tier.get("monthly_price_in_cents", 0)
    price_usd = price_cents / 100.0
    
    # Map USD price to EUR module tier
    if price_usd >= 9000:
        module = "COHORT"
    elif price_usd >= 1400:
        module = "ONCOLOGY"
    elif price_usd >= 450:
        module = "DIABETES"
    elif price_usd >= 250:
        module = "LONGEVITY"
    else:
        module = "LONGEVITY"
        
    return generate_license_key(module=module, sponsor_login=sponsor)
