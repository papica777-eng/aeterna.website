# =============================================================================
# === AETERNA VHT NEUROLOGICAL ENGINE: CONNECTOME & PLV MATRIX (MOJO CORE) ===
# =============================================================================
# Complexity: O(C^2 * N) / Vectorized Phase Locking Value (PLV) Analysis
# Module: connectome_plv_engine.mojo
# =============================================================================

from math import sin, cos, atan2, sqrt, pi
from collections import List

struct ConnectivityMatrix:
    var channel_names: List[String]
    var matrix: List[List[Float64]]
    var channel_count: Int

    fn __init__(out self, names: List[String]):
        self.channel_names = names
        self.channel_count = len(names)
        self.matrix = List[List[Float64]]()
        for i in range(self.channel_count):
            var row = List[Float64]()
            for j in range(self.channel_count):
                if i == j:
                    row.append(1.0)
                else:
                    row.append(0.0)
            self.matrix.append(row)

    fn set_plv(mut self, i: Int, j: Int, val: Float64):
        if i < self.channel_count and j < self.channel_count:
            self.matrix[i][j] = val
            self.matrix[j][i] = val

    fn print_matrix(self):
        print("=== [AETERNA CONNECTOME PLV FUNCTIONAL MATRIX] ===")
        for i in range(self.channel_count):
            var row_str: String = self.channel_names[i] + "\t| "
            for j in range(self.channel_count):
                var val_str = String(self.matrix[i][j])
                row_str += val_str + "\t"
            print(row_str)
        print("==================================================")


fn calculate_instantaneous_phase(signal: List[Float64]) -> List[Float64]:
    var n = len(signal)
    var phases = List[Float64]()
    if n == 0:
        return phases

    for i in range(n):
        var next_idx = i + 1 if i + 1 < n else i
        var prev_idx = i - 1 if i > 0 else 0
        var derivative = (signal[next_idx] - signal[prev_idx]) / 2.0
        var phase = atan2(derivative, signal[i])
        phases.append(phase)

    return phases


fn compute_pairwise_plv(signal_a: List[Float64], signal_b: List[Float64]) -> Float64:
    var n = min(len(signal_a), len(signal_b))
    if n == 0:
        return 0.0

    var phase_a = calculate_instantaneous_phase(signal_a)
    var phase_b = calculate_instantaneous_phase(signal_b)

    var sum_cos: Float64 = 0.0
    var sum_sin: Float64 = 0.0

    for t in range(n):
        var phase_diff = phase_a[t] - phase_b[t]
        sum_cos += cos(phase_diff)
        sum_sin += sin(phase_diff)

    var real_part = sum_cos / Float64(n)
    var imag_part = sum_sin / Float64(n)

    return sqrt(real_part * real_part + imag_part * imag_part)
