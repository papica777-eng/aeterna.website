//! Telemetry Module
//! High-performance, zero-allocation lock-free ring buffers for 
//! real-time security signal processing.

use crossbeam_queue::ArrayQueue;
use std::sync::Arc;

/// A lock-free ring buffer for processing high-frequency security events
pub struct TelemetryRingBuffer {
    queue: Arc<ArrayQueue<EventSignal>>,
}

#[derive(Debug, Clone)]
pub struct EventSignal {
    pub timestamp: u64,
    pub severity: u8,
    pub payload_hash: String,
}

impl TelemetryRingBuffer {
    pub fn new(capacity: usize) -> Self {
        TelemetryRingBuffer {
            queue: Arc::new(ArrayQueue::new(capacity)),
        }
    }

    /// Pushes an event in O(1) time without GC pauses
    pub fn push_event(&self, event: EventSignal) -> Result<(), EventSignal> {
        self.queue.push(event)
    }

    /// Processes events in batches for the AI Brain
    pub fn drain_batch(&self, batch_size: usize) -> Vec<EventSignal> {
        let mut batch = Vec::with_capacity(batch_size);
        while let Some(event) = self.queue.pop() {
            batch.push(event);
            if batch.len() >= batch_size {
                break;
            }
        }
        batch
    }
}
