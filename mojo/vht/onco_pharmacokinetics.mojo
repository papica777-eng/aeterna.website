# =============================================================================
# === AETERNA VHT ONCOLOGY ENGINE: 2-COMPARTMENT PHARMACOKINETICS (MOJO) ===
# =============================================================================
# Complexity: O(N) where N is number of simulation time-steps
# Based on: VHT_SYSTEMS.soul :: ORGAN_PHARMACOKINETICS & DRUG_REGISTRY
# Module: onco_pharmacokinetics.mojo
# =============================================================================

from math import exp, log
from collections import List

struct DrugProfile:
    var name: String
    var drug_class: String
    var molecular_weight_kda: Float64
    var blood_brain_barrier_penetration: Bool
    var elimination_rate_k10: Float64 # hr^-1
    var distribution_rate_k12: Float64 # hr^-1
    var redistribution_rate_k21: Float64 # hr^-1
    var central_volume_v1_liters: Float64
    var therapeutic_min_ug_ml: Float64
    var toxicity_max_ug_ml: Float64

    fn __init__(
        out self,
        name: String,
        drug_class: String,
        mw: Float64,
        bbb: Bool,
        k10: Float64,
        k12: Float64,
        k21: Float64,
        v1: Float64,
        c_min: Float64,
        c_max: Float64
    ):
        self.name = name
        self.drug_class = drug_class
        self.molecular_weight_kda = mw
        self.blood_brain_barrier_penetration = bbb
        self.elimination_rate_k10 = k10
        self.distribution_rate_k12 = k12
        self.redistribution_rate_k21 = k21
        self.central_volume_v1_liters = v1
        self.therapeutic_min_ug_ml = c_min
        self.toxicity_max_ug_ml = c_max


struct PKSimulationResult:
    var drug_name: String
    var peak_conc_cmax: Float64
    var time_to_peak_tmax: Float64
    var area_under_curve_auc: Float64
    var half_life_elimination_hours: Float64
    var brain_tissue_active: Bool

    fn print_summary(self):
        print("=== [AETERNA VHT ONCOLOGY PHARMACOKINETIC AUDIT] ===")
        print("Drug Candidate:          ", self.drug_name)
        print("Peak Concentration Cmax: ", self.peak_conc_cmax, "ug/mL")
        print("Time to Peak Tmax:       ", self.time_to_peak_tmax, "hours")
        print("AUC (0-24h):             ", self.area_under_curve_auc, "ug*hr/mL")
        print("Elimination Half-Life:   ", self.half_life_elimination_hours, "hours")
        print("Crosses BBB (Brain/CNS): ", self.brain_tissue_active)
        print("====================================================")


fn simulate_two_compartment_pk(
    drug: DrugProfile,
    dose_mg: Float64,
    total_hours: Float64,
    dt_hours: Float64
) -> PKSimulationResult:
    var steps = Int(total_hours / dt_hours)
    var c1: Float64 = dose_mg / drug.central_volume_v1_liters
    var c2: Float64 = 0.0

    var cmax: Float64 = c1
    var tmax: Float64 = 0.0
    var auc: Float64 = 0.0

    for i in range(steps):
        var t = Float64(i) * dt_hours
        var flux_10 = drug.elimination_rate_k10 * c1
        var flux_12 = drug.distribution_rate_k12 * c1
        var flux_21 = drug.redistribution_rate_k21 * c2

        var dc1 = (-flux_10 - flux_12 + flux_21) * dt_hours
        var dc2 = (flux_12 - flux_21) * dt_hours

        c1 += dc1
        c2 += dc2

        if c1 > cmax:
            cmax = c1
            tmax = t

        auc += c1 * dt_hours

    var half_life = log(2.0) / drug.elimination_rate_k10

    return PKSimulationResult(
        drug.name,
        cmax,
        tmax,
        auc,
        half_life,
        drug.blood_brain_barrier_penetration
    )


fn main():
    print("Initializing AETERNA VHT Precision Oncology PK/PD Engine...")
    var osimertinib = DrugProfile("Osimertinib", "EGFR_TKI_G3", 0.50, True, 0.015, 0.080, 0.040, 40.0, 0.15, 2.50)
    var res_osi = simulate_two_compartment_pk(osimertinib, 80.0, 48.0, 0.1)
    res_osi.print_summary()
