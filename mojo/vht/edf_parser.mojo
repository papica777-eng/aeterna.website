# =============================================================================
# === AETERNA VHT NEUROLOGICAL ENGINE: EDF/EDF+ BINARY PARSER (MOJO CORE) ===
# =============================================================================
# Complexity: O(N) where N is number of data samples
# Specification: European Data Format (EDF / EDF+ standard for biosignals)
# Module: edf_parser.mojo
# =============================================================================

from collections import List

struct EDFSignalHeader:
    var label: String
    var transducer_type: String
    var physical_dimension: String
    var physical_min: Float64
    var physical_max: Float64
    var digital_min: Int
    var digital_max: Int
    var prefiltering: String
    var sample_count_per_record: Int

    fn __init__(
        out self,
        label: String,
        transducer: String,
        dim: String,
        p_min: Float64,
        p_max: Float64,
        d_min: Int,
        d_max: Int,
        prefilt: String,
        samples_per_rec: Int
    ):
        self.label = label
        self.transducer_type = transducer
        self.physical_dimension = dim
        self.physical_min = p_min
        self.physical_max = p_max
        self.digital_min = d_min
        self.digital_max = d_max
        self.prefiltering = prefilt
        self.sample_count_per_record = samples_per_rec

    fn digital_to_physical(self, digital_val: Int) -> Float64:
        var d_span = Float64(self.digital_max - self.digital_min)
        if d_span == 0.0:
            return 0.0
        var p_span = self.physical_max - self.physical_min
        var normalized = Float64(digital_val - self.digital_min) / d_span
        return normalized * p_span + self.physical_min
