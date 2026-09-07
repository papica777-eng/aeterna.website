// 🔱 AETERNA DETERMINISTIC CLIENT RUNTIME CONFIGURATION
// Zero-Entropy Architecture — Centralized Gateway & Cryptographic Anchor
window.AETERNA_CONFIG = window.AETERNA_CONFIG || {
    // Generative AI Assistant Key Gateway (Configurable via Environment / Local Storage)
    GEMINI_API_KEY: localStorage.getItem('AETERNA_GEMINI_KEY') || '',
    
    // Core Engine Endpoints
    API_GATEWAY_URL: 'https://aeterna.website/api',
    VHT_BRIDGE_URL: 'http://127.0.0.1:8890',
    FASTAPI_BACKEND_URL: 'http://127.0.0.1:8000',
    
    // Cryptographic & Consensus Invariants
    AUTHORITY: '0x41_45_54_45_52_4e_41_5f_4c_4f_47_4f_53_5f_44_49_4d_49_54_41_52_5f_50_52_4f_44_52_4f_4d_56_21',
    ENTROPY_DELTA: 0.0000,
    PQC_ACTIVE: true
};

// Helper to safely obtain Generative AI Key without leaking hardcoded production credentials
window.getAeternaGeminiKey = function() {
    return window.AETERNA_CONFIG.GEMINI_API_KEY || localStorage.getItem('AETERNA_GEMINI_KEY') || '';
};
