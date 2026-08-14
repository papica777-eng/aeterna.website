"""
=============================================================================
=== AETERNA VHT LIVE REST BRIDGE E2E VERIFICATION TEST RUNNER ===
=============================================================================
Author: Dimitar Stavrev Prodromov (Lead Architect, AETERNA)
Target: http://127.0.0.1:8890
Verifications: Health, Patients API, RK4 PK/PD Simulation, Pan-Tompkins ECG
=============================================================================
"""

import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:8890"

def test_health():
    print("[E2E TEST 1] GET /api/v1/health ...")
    req = urllib.request.Request(f"{BASE_URL}/api/v1/health")
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected 200, got {res.status}"
        data = json.loads(res.read().decode())
        assert data["status"] == "ONLINE", "Status is not ONLINE"
        assert "PanTompkinsECG" in data["active_engines"], "Missing PanTompkinsECG engine"
        print(f"  -> Health check PASSED: Status {data['status']} | Substrate: {data['substrate']}")

def test_patient_api():
    print("[E2E TEST 2] GET /api/v1/patients/K-902 ...")
    req = urllib.request.Request(f"{BASE_URL}/api/v1/patients/K-902")
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected 200, got {res.status}"
        data = json.loads(res.read().decode())
        assert data["patient_id"] == "Patient_K-902", "Patient ID mismatch"
        print(f"  -> Patient K-902 PASSED: Disease: {data['name']} | Driver: {data['driver_mutations']}")

def test_pkpd_simulation():
    print("[E2E TEST 3] POST /api/v1/pkpd/simulate (Osimertinib 80mg) ...")
    payload = json.dumps({"drug": "OSIMERTINIB", "dose_mg": 80.0, "hours": 48.0}).encode()
    req = urllib.request.Request(f"{BASE_URL}/api/v1/pkpd/simulate", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected 200, got {res.status}"
        data = json.loads(res.read().decode())
        assert data["cmax_ug_ml"] > 1.5, f"Cmax {data['cmax_ug_ml']} below therapeutic threshold"
        assert len(data["time_series"]["central_plasma_ug_ml"]) > 50, "Time series data too short"
        print(f"  -> PK/PD RK4 PASSED: Cmax: {data['cmax_ug_ml']} ug/mL | AUC: {data['auc_ug_hr_ml']} ug*hr/mL | Half-Life: {data['elimination_half_life_hours']}h")

def test_pan_tompkins_ecg():
    print("[E2E TEST 4] POST /api/v1/cardio/ecg (Pan-Tompkins QRS & HRV) ...")
    req = urllib.request.Request(f"{BASE_URL}/api/v1/cardio/ecg", data=b"{}", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected 200, got {res.status}"
        data = json.loads(res.read().decode())
        assert data["status"] == "VALID", "HRV analysis invalid"
        assert 60.0 <= data["heart_rate_bpm"] <= 85.0, f"Heart rate {data['heart_rate_bpm']} out of expected range"
        print(f"  -> Pan-Tompkins ECG PASSED: Heart Rate: {data['heart_rate_bpm']} BPM | SDNN: {data['sdnn_ms']} ms | RMSSD: {data['rmssd_ms']} ms | Class: {data['arrhythmia_classification']}")

def test_tumor_lysis_sweep():
    print("[E2E TEST 5] POST /api/v1/lysis/sweep (Patient K-902) ...")
    payload = json.dumps({"patient_id": "K-902", "drug_efficacy": 1.0}).encode()
    req = urllib.request.Request(f"{BASE_URL}/api/v1/lysis/sweep", data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected 200, got {res.status}"
        data = json.loads(res.read().decode())
        assert data["overall_regression_recist_pct"] > 50.0, "Regression rate below expected response"
        print(f"  -> Cytolysis Sweep PASSED: RECIST Tumor Regression: -{data['overall_regression_recist_pct']}% | Outcome: {data['therapeutic_outcome']}")

if __name__ == "__main__":
    print("======================================================================")
    print("  🔱 RUNNING LIVE VHT BRIDGE REST API E2E VERIFICATION SUITE         ")
    print("======================================================================")
    t0 = time.time()
    test_health()
    test_patient_api()
    test_pkpd_simulation()
    test_pan_tompkins_ecg()
    test_tumor_lysis_sweep()
    t_total = (time.time() - t0) * 1000.0
    print("======================================================================")
    print(f"  STATUS: ALL 5 E2E TESTS PASSED IN {t_total:.2f} ms // ZERO DEFECTS")
    print("======================================================================")
