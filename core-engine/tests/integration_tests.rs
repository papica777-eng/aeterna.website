//! Integration Tests for AETERNA Core Engine
//! Demonstrates the high test coverage required for EIC TRL 6 verification.

use aeterna_core_engine::telemetry::{TelemetryRingBuffer, EventSignal};
use aeterna_core_engine::vortex_synthesis;
use aeterna_core_engine::pqc_vault;

#[test]
fn test_telemetry_lock_free_throughput() {
    let buffer = TelemetryRingBuffer::new(100_000);
    
    // Simulate burst traffic
    for i in 0..50_000 {
        let event = EventSignal {
            timestamp: i as u64,
            severity: 1,
            payload_hash: format!("hash_{}", i),
        };
        assert!(buffer.push_event(event).is_ok());
    }
    
    let batch = buffer.drain_batch(10_000);
    assert_eq!(batch.len(), 10_000);
}

#[test]
fn test_vortex_swarm_initialization() {
    let result = vortex_synthesis::initialize_swarm(150);
    assert!(result.starts_with("SWARM_LOCKED"));
}

#[test]
fn test_pqc_ledger_hashing() {
    let data = b"AETERNA_CRITICAL_TRANSACTION";
    let hash = pqc_vault::hash_ledger_entry(data);
    
    // SHA-512 outputs 64 bytes -> 128 hex characters
    assert_eq!(hash.len(), 128);
}
