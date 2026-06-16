// ═══════════════════════════════════════════════════════════════════════════════
// AETERNA VIVISECTOR — WASM Bridge Layer
// ═══════════════════════════════════════════════════════════════════════════════
// This module loads the compiled vivisector_core.wasm binary and provides
// a clean async API for the HTML frontend. The scan engine is opaque —
// all pattern matching, severity classification, and Catuṣkoṭi logic
// lives inside the WASM binary, invisible to DevTools.
//
// Without a valid Ignition Key, the engine returns ZERO findings.
// The HTML/JS frontend is a "dead shell" without this module.
// ═══════════════════════════════════════════════════════════════════════════════

const WasmEngine = (() => {
    // ─── State ────────────────────────────────────────────────────────────────
    let wasmInstance = null;
    let wasmMemory = null;
    let isLoaded = false;
    let isUnlocked = false;

    const encoder = new TextEncoder();
    const decoder = new TextDecoder();

    // ─── Load WASM Module ─────────────────────────────────────────────────────
    async function init() {
        try {
            const response = await fetch('vivisector_core.wasm?v=' + Date.now());
            if (!response.ok) {
                console.warn('[WASM_BRIDGE] vivisector_core.wasm not found. Running in FALLBACK JS mode.');
                isLoaded = false;
                return false;
            }

            const bytes = await response.arrayBuffer();

            // Instantiate with memory import
            wasmMemory = new WebAssembly.Memory({
                initial: 64,  // 64 pages = 4MB
                maximum: 256, // 256 pages = 16MB max
            });

            const importObject = {
                env: {
                    memory: wasmMemory,
                },
            };

            const result = await WebAssembly.instantiate(bytes, importObject);
            wasmInstance = result.instance;
            if (typeof window !== 'undefined') {
                window.debugWasmInstance = wasmInstance;
            } else {
                self.debugWasmInstance = wasmInstance;
            }
            isLoaded = true;

            const version = wasmInstance.exports.get_version();
            const major = (version >> 16) & 0xFF;
            const minor = (version >> 8) & 0xFF;
            const patch = version & 0xFF;
            console.log(`[WASM_BRIDGE] vivisector_core.wasm loaded. v${major}.${minor}.${patch}`);
            console.log(`[WASM_BRIDGE] ${wasmInstance.exports.get_scan_rules_count()} scan rules compiled into binary.`);

            return true;
        } catch (err) {
            console.error('[WASM_BRIDGE] Failed to load WASM:', err);
            isLoaded = false;
            return false;
        }
    }

    // ─── Ignition Key & Dynamic SOUL Rules (Phase 3) ─────────────────────────
    function unlock(sessionToken, encryptedPayloadBase64) {
        if (!isLoaded) return false;

        const tokenBytes = encoder.encode(sessionToken);
        const ptr = wasmInstance.exports.wasm_alloc(tokenBytes.length);
        if (ptr === 0) return false;

        // Write token into WASM memory
        const mem = new Uint8Array(wasmInstance.exports.memory.buffer);
        mem.set(tokenBytes, ptr);

        const result = wasmInstance.exports.unlock_engine(ptr, tokenBytes.length);
        wasmInstance.exports.wasm_free(ptr, tokenBytes.length);

        if (result !== 1) {
            isUnlocked = false;
            return false;
        }

        // If encrypted SOUL payload is provided, decrypt and parse in WASM memory dynamically
        if (encryptedPayloadBase64) {
            try {
                const binString = atob(encryptedPayloadBase64);
                const payloadBytes = Uint8Array.from(binString, (m) => m.codePointAt(0));

                const payloadPtr = wasmInstance.exports.wasm_alloc(payloadBytes.length);
                const keyPtr = wasmInstance.exports.wasm_alloc(tokenBytes.length);

                if (payloadPtr === 0 || keyPtr === 0) {
                    console.error('[WASM_BRIDGE] OOM: Failed to allocate payload or key buffers.');
                    isUnlocked = false;
                    return false;
                }

                // Write key and payload to WASM memory
                const dynamicMem = new Uint8Array(wasmInstance.exports.memory.buffer);
                dynamicMem.set(payloadBytes, payloadPtr);
                dynamicMem.set(tokenBytes, keyPtr);

                const decryptResult = wasmInstance.exports.load_encrypted_payload(
                    payloadPtr,
                    payloadBytes.length,
                    keyPtr,
                    tokenBytes.length
                );

                wasmInstance.exports.wasm_free(payloadPtr, payloadBytes.length);
                wasmInstance.exports.wasm_free(keyPtr, tokenBytes.length);

                isUnlocked = decryptResult === 1;
                if (isUnlocked) {
                    console.log(`[WASM_BRIDGE] Dynamic SOUL payload loaded. ${wasmInstance.exports.get_scan_rules_count()} rules initialized in-memory.`);
                }
                return isUnlocked;
            } catch (err) {
                console.error('[WASM_BRIDGE] Failed to load/decrypt dynamic SOUL rules payload:', err);
                isUnlocked = false;
                return false;
            }
        }

        isUnlocked = true;
        return isUnlocked;
    }

    function lock() {
        if (!isLoaded) return;
        wasmInstance.exports.lock_engine();
        isUnlocked = false;
    }

    // ─── Scan File ────────────────────────────────────────────────────────────
    function scanFile(fileText) {
        if (!isLoaded) {
            console.warn('[WASM_BRIDGE] Engine not loaded. Using JS fallback.');
            return null; // Signal to use JS fallback
        }

        // Reset allocator for fresh scan
        wasmInstance.exports.wasm_reset();

        const textBytes = encoder.encode(fileText);
        const ptr = wasmInstance.exports.wasm_alloc(textBytes.length);
        if (ptr === 0) {
            console.error('[WASM_BRIDGE] OOM: Cannot allocate buffer for file.');
            return [];
        }

        // Write file content into WASM memory
        const mem = new Uint8Array(wasmInstance.exports.memory.buffer);
        mem.set(textBytes, ptr);

        // Execute scan (returns finding count)
        const count = wasmInstance.exports.scan_buffer(ptr, textBytes.length);

        if (count === 0) return [];

        // Read JSON output from WASM output buffer
        const outputPtr = wasmInstance.exports.get_output_ptr();
        const outputLen = wasmInstance.exports.get_output_len();

        // Re-read memory (may have grown)
        const outputMem = new Uint8Array(wasmInstance.exports.memory.buffer);
        const jsonBytes = outputMem.slice(outputPtr, outputPtr + outputLen);
        const jsonStr = decoder.decode(jsonBytes);

        try {
            return JSON.parse(jsonStr);
        } catch (err) {
            console.error('[WASM_BRIDGE] Failed to parse findings JSON:', err);
            return [];
        }
    }

    // ─── Utility Getters ──────────────────────────────────────────────────────
    function getRulesCount() {
        if (!isLoaded) return 0;
        return wasmInstance.exports.get_scan_rules_count();
    }

    function getVersion() {
        if (!isLoaded) return '0.0.0';
        const v = wasmInstance.exports.get_version();
        return `${(v >> 16) & 0xFF}.${(v >> 8) & 0xFF}.${v & 0xFF}`;
    }

    function getStorageOffset() {
        if (!isLoaded) return 0;
        return wasmInstance.exports.get_rules_storage_offset ? wasmInstance.exports.get_rules_storage_offset() : 0;
    }

    function getStorageCapacity() {
        if (!isLoaded) return 0;
        return wasmInstance.exports.get_rules_storage_capacity ? wasmInstance.exports.get_rules_storage_capacity() : 65536;
    }

    // ─── Catuṣkoṭi State Names ───────────────────────────────────────────────
    const CATUSKOTI_NAMES = ['CONFIRMED', 'MITIGATED', 'PARADOX', 'ZERO_DAY'];
    const CATUSKOTI_SANSKRIT = ['CONFIRMED', 'MITIGATED', 'PARADOX', 'ZERO_DAY'];
    const CATUSKOTI_COLORS = ['emerald', 'cyan', 'yellow', 'red'];

    function getCatuskotiName(state) {
        return CATUSKOTI_NAMES[state] || 'UNKNOWN';
    }
    function getCatuskotiSanskrit(state) {
        return CATUSKOTI_SANSKRIT[state] || '?';
    }
    function getCatuskotiColor(state) {
        return CATUSKOTI_COLORS[state] || 'gray';
    }

    // ─── Public API ───────────────────────────────────────────────────────────
    return {
        init,
        unlock,
        lock,
        scanFile,
        getRulesCount,
        getVersion,
        getStorageOffset,
        getStorageCapacity,
        getCatuskotiName,
        getCatuskotiSanskrit,
        getCatuskotiColor,
        get isLoaded() { return isLoaded; },
        get isUnlocked() { return isUnlocked; },
        CATUSKOTI_NAMES,
        CATUSKOTI_SANSKRIT,
    };
})();
