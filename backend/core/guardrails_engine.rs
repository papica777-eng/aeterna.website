// ═══════════════════════════════════════════════════════════════════════════════
// === guardrails_engine.rs — Rust Guardrails Classifier ===
// ═══════════════════════════════════════════════════════════════════════════════
// Path:       backend/core/guardrails_engine.rs
// Architect:  Dimitar Prodromov
// Purpose:    High-performance topic classification for the Clinical Copilot.
//             Compiles to native binary, called from Python orchestrator via FFI.
//             Production replacement for guardrails.py keyword matching.
//
// Complexity: O(k) where k = number of keywords per check
// Safety:     No unsafe blocks. Pure deterministic logic.
// Build:      rustc guardrails_engine.rs --edition 2021 -o guardrails_engine
//             OR: cargo build --release (with Cargo.toml)
// ═══════════════════════════════════════════════════════════════════════════════

use std::collections::HashSet;

/// Catuskoti classification states for topic analysis
#[derive(Debug, Clone, PartialEq)]
pub enum TopicVerdict {
    /// TRUE: Question is definitively on-topic (keyword match)
    OnTopic { confidence: f64, matched_domain: String },
    /// FALSE: Question is definitively off-topic (forbidden keyword)
    OffTopic { reason: String },
    /// BOTH: Ambiguous — partially on-topic, needs vector verification
    Ambiguous { similarity_required: bool },
    /// NEITHER: Cannot determine — fallback to vector threshold
    Unknown,
}

/// Language detection result
#[derive(Debug, Clone, PartialEq)]
pub enum Language {
    Bulgarian,
    English,
}

/// Core guardrails engine — deterministic topic classifier
pub struct GuardrailsEngine {
    on_topic_keywords: HashSet<String>,
    off_topic_keywords: HashSet<String>,
    similarity_threshold: f64,
}

impl GuardrailsEngine {
    // Complexity: O(k1 + k2) where k1, k2 = keyword set sizes
    pub fn new() -> Self {
        let on_topic: Vec<&str> = vec![
            // Core architecture
            "vht", "aeterna", "virtual human twin", "digital twin",
            "zero-entropy", "sovereign", "детерминист", "дигитален близнак",
            // Clinical oncology
            "c-index", "concordance", "апоптоз", "apoptosis", "kras", "tp53",
            "p53", "brca", "egfr", "мутаци", "mutation", "онколог", "oncolog",
            "tumor", "тумор", "рак", "cancer", "химиотерапи", "chemotherap",
            "имунотерап", "immunotherap", "лъчетерап", "radiotherap",
            // Standards & Regulatory
            "loinc", "fhir", "hl7", "eu mdr", "class iii", "iso 13485",
            "iso 14971", "gdpr", "eu ai act", "clinical trial", "клинично изпитване",
            // Survival metrics
            "преживяемост", "survival", "hazard", "kaplan-meier", "cox",
            "auc", "roc", "сенситивност", "sensitivity", "специфичност",
            // Brain module
            "brain", "мозък", "перфузи", "perfusion", "cbf", "синаптич", "synaptic",
            // Cardio module
            "кардио", "cardio", "сърд", "heart", "ecg", "ekg", "ejection fraction",
            // Diabetes module
            "диабет", "diabetes", "hba1c", "глюкоз", "glucose", "инсулин", "insulin",
            // Platform & EIC
            "trl", "eic", "horizon", "accelerator", "work package",
            "партньор", "partner", "consortium", "координатор",
            // Smart infrastructure
            "smart city", "submarine cable", "подводен кабел", "интелигентен град",
        ];

        let off_topic: Vec<&str> = vec![
            "рецепта за", "recipe", "готварс", "cooking", "футбол", "football",
            "soccer", "време", "weather", "филм", "movie", "музика", "music",
            "игра", "game", "спорт", "sport", "политик", "politic",
            "крипто", "crypto", "bitcoin", "биткойн", "ethereum",
            "maglev", "левитира",
        ];

        Self {
            on_topic_keywords: on_topic.into_iter().map(String::from).collect(),
            off_topic_keywords: off_topic.into_iter().map(String::from).collect(),
            similarity_threshold: 0.30,
        }
    }

    /// Detect language from text — O(n) where n = text length
    pub fn detect_language(&self, text: &str) -> Language {
        let cyrillic_count = text.chars()
            .filter(|c| ('\u{0400}'..='\u{04FF}').contains(c))
            .count();
        let total = text.chars().count().max(1);

        if cyrillic_count as f64 / total as f64 > 0.3 {
            Language::Bulgarian
        } else {
            Language::English
        }
    }

    /// Classify a question — O(k) where k = total keywords
    pub fn classify(&self, question: &str, top_similarity: f64) -> TopicVerdict {
        let lower = question.to_lowercase();

        // Phase 1: Hard reject — explicit off-topic keywords
        for kw in &self.off_topic_keywords {
            if lower.contains(kw.as_str()) {
                return TopicVerdict::OffTopic {
                    reason: format!("Matched forbidden keyword: '{}'", kw),
                };
            }
        }

        // Phase 2: Strong accept — explicit on-topic keywords
        for kw in &self.on_topic_keywords {
            if lower.contains(kw.as_str()) {
                return TopicVerdict::OnTopic {
                    confidence: 0.95,
                    matched_domain: kw.clone(),
                };
            }
        }

        // Phase 3: Vector similarity fallback
        if top_similarity >= self.similarity_threshold {
            TopicVerdict::OnTopic {
                confidence: top_similarity,
                matched_domain: "vector_match".to_string(),
            }
        } else if top_similarity >= 0.15 {
            TopicVerdict::Ambiguous {
                similarity_required: true,
            }
        } else {
            TopicVerdict::OffTopic {
                reason: format!(
                    "Below similarity threshold: {:.3} < {:.3}",
                    top_similarity, self.similarity_threshold
                ),
            }
        }
    }
}

// ── CLI Entry Point (for subprocess calls from Python) ───────────────────────
fn main() {
    let args: Vec<String> = std::env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: guardrails_engine <question> [similarity_score]");
        std::process::exit(1);
    }

    let question = &args[1];
    let similarity: f64 = args.get(2)
        .and_then(|s| s.parse().ok())
        .unwrap_or(0.0);

    let engine = GuardrailsEngine::new();
    let lang = engine.detect_language(question);
    let verdict = engine.classify(question, similarity);

    // Output JSON for Python consumption
    println!(
        "{{\"verdict\":\"{:?}\",\"language\":\"{:?}\",\"query\":\"{}\"}}",
        verdict, lang, question.replace('"', "\\\"")
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_on_topic_cindex() {
        let engine = GuardrailsEngine::new();
        let result = engine.classify("Как работи C-Index 0.9713?", 0.0);
        assert!(matches!(result, TopicVerdict::OnTopic { .. }));
    }

    #[test]
    fn test_off_topic_cooking() {
        let engine = GuardrailsEngine::new();
        let result = engine.classify("Дай ми рецепта за боб", 0.0);
        assert!(matches!(result, TopicVerdict::OffTopic { .. }));
    }

    #[test]
    fn test_language_detection_bg() {
        let engine = GuardrailsEngine::new();
        assert_eq!(engine.detect_language("Здравейте доктор"), Language::Bulgarian);
    }

    #[test]
    fn test_language_detection_en() {
        let engine = GuardrailsEngine::new();
        assert_eq!(engine.detect_language("Hello doctor"), Language::English);
    }

    #[test]
    fn test_vector_threshold_accept() {
        let engine = GuardrailsEngine::new();
        let result = engine.classify("some ambiguous question", 0.45);
        assert!(matches!(result, TopicVerdict::OnTopic { .. }));
    }

    #[test]
    fn test_vector_threshold_reject() {
        let engine = GuardrailsEngine::new();
        let result = engine.classify("some random text", 0.05);
        assert!(matches!(result, TopicVerdict::OffTopic { .. }));
    }
}
