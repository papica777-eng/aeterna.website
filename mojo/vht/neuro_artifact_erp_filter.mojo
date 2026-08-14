# =============================================================================
# === AETERNA VHT NEUROLOGICAL ENGINE: ARTIFACT FILTER & ERP DETECTOR (MOJO) ===
# =============================================================================
# Complexity: O(N) / Z-Score Adaptive Thresholding & Event-Related Potentials
# Module: neuro_artifact_erp_filter.mojo
# =============================================================================

from math import sqrt
from collections import List

struct ERPDetectionResult:
    var peak_latency_ms: Float64
    var peak_amplitude_uv: Float64
    var p300_detected: Bool
    var confidence_score: Float64

    fn __init__(out self, latency: Float64, amplitude: Float64, detected: Bool, confidence: Float64):
        self.peak_latency_ms = latency
        self.peak_amplitude_uv = amplitude
        self.p300_detected = detected
        self.confidence_score = confidence


struct ArtifactFilterStats:
    var original_sample_count: Int
    var rejected_artifact_count: Int
    var clean_ratio_pct: Float64

    fn __init__(out self, orig: Int, rejected: Int):
        self.original_sample_count = orig
        self.rejected_artifact_count = rejected
        if orig > 0:
            self.clean_ratio_pct = (Float64(orig - rejected) / Float64(orig)) * 100.0
        else:
            self.clean_ratio_pct = 0.0


fn suppress_ocular_artifacts(raw_signal: List[Float64], z_threshold: Float64) -> Tuple[List[Float64], ArtifactFilterStats]:
    var n = len(raw_signal)
    var clean_signal = List[Float64]()
    if n == 0:
        return clean_signal, ArtifactFilterStats(0, 0)

    var sum_val: Float64 = 0.0
    for i in range(n):
        sum_val += raw_signal[i]
    var mean = sum_val / Float64(n)

    var sum_sq_diff: Float64 = 0.0
    for i in range(n):
        var diff = raw_signal[i] - mean
        sum_sq_diff += diff * diff
    var std_dev = sqrt(sum_sq_diff / Float64(n))
    if std_dev == 0.0:
        std_dev = 1.0

    var rejected_count = 0
    for i in range(n):
        var z_score = (raw_signal[i] - mean) / std_dev
        if z_score > z_threshold or z_score < -z_threshold:
            clean_signal.append(mean)
            rejected_count += 1
        else:
            clean_signal.append(raw_signal[i])

    return clean_signal, ArtifactFilterStats(n, rejected_count)
