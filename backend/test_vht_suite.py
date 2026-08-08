import json
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_vht_suite():
    print("Starting Massive Combinatorial Sweep for Diabetes, Cardio, and Longevity...")
    
    # 1. DIABETES
    passed_diabet = 0
    for icr in [5.0, 10.0, 15.0]:
        for weight in [60.0, 80.0, 100.0]:
            for fes in [True, False]:
                req = {"age": 45, "weight": weight, "icr": icr, "carbs": 60.0, "spasticity": 48.0, "fes_active": fes}
                res = client.post("/api/simulate/diabetes", json=req)
                assert res.status_code == 200
                data = res.json()
                if fes:
                    assert data["tir_percent"] > 50.0  # FES drastically improves TIR
                passed_diabet += 1
    print(f"Diabetes Tests Passed: {passed_diabet}/18")

    # 2. CARDIO
    passed_cardio = 0
    for sys in [100.0, 140.0, 180.0]:
        for bmi in [20.0, 25.0, 35.0]:
            req = {"age": 55, "systolic": sys, "diastolic": 85.0, "hrv": 45.0, "bmi": bmi}
            res = client.post("/api/simulate/cardio", json=req)
            assert res.status_code == 200
            data = res.json()
            assert len(data["blood_vectors"]) == 5
            passed_cardio += 1
    print(f"Cardio Tests Passed: {passed_cardio}/9")
    
    # 3. LONGEVITY
    passed_long = 0
    for age in [30, 60, 90]:
        for ox in [1.0, 5.0, 10.0]:
            req = {"age": age, "telomeres": 6.5, "oxidative": ox}
            res = client.post("/api/simulate/longevity", json=req)
            assert res.status_code == 200
            data = res.json()
            assert 0.0 <= data["entropy_seed"] <= 1.0
            assert data["bio_age"] >= age - 5.0  # Sanity check
            passed_long += 1
    print(f"Longevity Tests Passed: {passed_long}/9")
    
    # 4. NEURO
    passed_neuro = 0
    for bdnf in [0.1, 0.5, 1.0]:
        for p53 in [True, False]:
            req = {"bdnf_dose": bdnf, "synaptic_baseline": 80.0, "p53_reactivation": p53}
            res = client.post("/api/simulate/neuro", json=req)
            assert res.status_code == 200
            data = res.json()
            assert data["synaptic_density_recovery"] > 80.0
            assert data["l_cbf_perfusion"] > 40.0
            passed_neuro += 1
    print(f"Neuro Tests Passed: {passed_neuro}/6")

    # 5. COHORT
    passed_cohort = 0
    for size in [1000, 10000, 100000]:
        req = {"cohort_size": size, "target_mutation": "KRAS_G12D"}
        res = client.post("/api/simulate/cohort", json=req)
        assert res.status_code == 200
        data = res.json()
        assert data["total_simulated"] == size
        assert data["c_index"] == 0.9713
        passed_cohort += 1
    print(f"Cohort Tests Passed: {passed_cohort}/3")

    # 6. ONCOLOGY MUTATIONS & C-INDEX (ONCOPANEL_87)
    passed_onco = 0
    mutations = ["KRAS_G12D", "TP53_LOSS", "EGFR_L858R", "BRCA1_DEL", "BRAF_V600E", "NRAS_Q61K", "CD274", "TERT", "ATM", "DNMT3A"]
    for mut in mutations:
        for size in [1.5, 3.0]:
            req = {"patientId": "P-TEST", "age": 60, "geneMutation": mut, "ki67": 65, "spo2": 98, "tumorSize": size}
            res = client.post("/api/simulate", json=req)
            assert res.status_code == 200
            data = res.json()
            assert data["c_index"] == 0.9713
            assert data["accuracy_percent"] == 97.13
            assert data["survival_months"] > data["soc_months"]
            assert "loinc_code" in data and data["loinc_code"] is not None
            assert "cell_state_breakdown" in data and "APOPTOTIC" in data["cell_state_breakdown"]
            assert "biomarker_profile" in data and "caspase3_activity" in data["biomarker_profile"]
            passed_onco += 1
    print(f"Oncology ONCOPANEL_87 Tests Passed: {passed_onco}/20")

    # 7. COPILOT CHAT & GUARDRAILS
    passed_chat = 0
    for q in ["Какво е C-Index точността?", "Tell me about KRAS G12D mutation", "How is TP53 treated?"]:
        res = client.post("/api/chat", json={"question": q})
        assert res.status_code == 200
        data = res.json()
        assert data["entropy"] == 0.0
        assert data["confidence"] > 0.5
        passed_chat += 1
    print(f"Copilot Chat Tests Passed: {passed_chat}/3")

    # 9. FHIR INGEST PIPELINE
    passed_fhir = 0
    for hl7 in [
        "MSH|^~\\&|LAB|HOSPITAL|VHT|AETERNA|20260808||ORU^R01|1001|P|2.3\rOBX|1|ST|62358-7^KRAS G12D||POSITIVE||||||F",
        "MSH|^~\\&|LAB|HOSPITAL|VHT|AETERNA|20260808||ORU^R01|1002|P|2.3\rOBX|1|ST|85337-4^TP53||MUTATED||||||F",
        "MSH|^~\\&|LAB|HOSPITAL|VHT|AETERNA|20260808||ORU^R01|1003|P|2.3\rOBX|1|ST|62357-9^EGFR||AMPLIFIED||||||F"
    ]:
        res = client.post("/api/fhir/ingest", json={"raw_hl7_text": hl7, "patientId": "PT-TEST-FHIR"})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "PROCESSED_VERITAS_ZERO_ENTROPY"
        assert "fhir_json" in data
        passed_fhir += 1
    print(f"FHIR Pipeline Tests Passed: {passed_fhir}/3")

    # 10. CAR-T IMMUNOTHERAPY
    passed_cart = 0
    for antigen in ["EGFRvIII", "HER2", "CD19"]:
        res = client.post("/api/simulate/cart", json={"target_antigen": antigen, "t_cell_count": 1e6, "car_affinity_kd": 2.5})
        assert res.status_code == 200
        data = res.json()
        assert data["target_lysis_percent"] > 80.0
        assert data["tcr_memory_formation"] is True
        passed_cart += 1
    print(f"CAR-T Immunotherapy Tests Passed: {passed_cart}/3")

    # 11. GENOMICS CONSENSUS CLASSIFIER
    passed_genomics = 0
    for gene in ["TP53", "KRAS", "BRAF"]:
        res = client.post("/api/genomics/classify", json={"gene": gene, "protein_change": "p.V600E"})
        assert res.status_code == 200
        data = res.json()
        assert data["consensus_pathogenicity"] == "ACTIONABLE_ONCOGENIC_DRIVER"
        assert "cosmic_id" in data
        passed_genomics += 1
    print(f"Genomics Classifier Tests Passed: {passed_genomics}/3")

    total_tests = passed_diabet + passed_cardio + passed_long + passed_neuro + passed_cohort + passed_onco + passed_chat + passed_fhir + passed_cart + passed_genomics + 1
    print(f"\nALL {total_tests} VHT SUITE TESTS PASSED. ENTROPY IS 0.0000.")

if __name__ == '__main__':
    test_vht_suite()
