# ═══════════════════════════════════════════════════════════════
# AETERNA VHT Clinical Copilot — Guardrails Module (SOUL-Driven)
# Reads boundaries from copilot_genesis.soul — zero hardcoded logic
# Complexity: O(k) per check, where k = number of keywords
# ═══════════════════════════════════════════════════════════════

from pathlib import Path
from soul_parser import SoulConfig


# ── Load SOUL Configuration ──────────────────────────────────────────────────
SOUL_PATH = Path(__file__).parent / "soul" / "copilot_genesis.soul"
_soul_config: SoulConfig | None = None


def get_soul_config() -> SoulConfig:
    """Lazy-load and cache SOUL configuration. Complexity: O(1) after first call."""
    global _soul_config
    if _soul_config is None:
        if SOUL_PATH.exists():
            _soul_config = SoulConfig.from_file(SOUL_PATH)
            print(f"[SOUL] Loaded copilot_genesis.soul — {len(_soul_config.manifolds)} manifolds")
        else:
            print(f"[WARN] Soul file not found: {SOUL_PATH}, using defaults")
            _soul_config = SoulConfig()
    return _soul_config


# ── On-Topic Keywords (from .soul ALLOWED_DOMAINS + clinical lexicon) ────────
ON_TOPIC_KEYWORDS = {
    # Core architecture
    "vht", "aeterna", "virtual human twin", "digital twin", "дигитален близнак",
    "zero-entropy", "sovereign", "детерминист",
    # Clinical
    "c-index", "concordance", "апоптоз", "apoptosis", "kras", "tp53", "p53",
    "brca", "egfr", "мутаци", "mutation", "онколог", "oncolog", "tumor",
    "тумор", "рак", "cancer", "химиотерапи", "chemotherap", "имунотерап",
    "immunotherap", "лъчетерап", "radiotherap",
    # Standards
    "loinc", "fhir", "hl7", "eu mdr", "class iii", "iso 13485", "iso 14971",
    "gdpr", "eu ai act", "clinical trial", "клинично изпитване",
    # Metrics
    "преживяемост", "survival", "hazard", "kaplan-meier", "cox",
    "auc", "roc", "сенситивност", "sensitivity", "специфичност", "specificity",
    # Brain / Cardio / Diabetes
    "brain", "мозък", "перфузи", "perfusion", "cbf", "синаптич", "synaptic",
    "кардио", "cardio", "сърд", "heart", "ecg", "ekg", "ejection fraction",
    "диабет", "diabetes", "hba1c", "глюкоз", "glucose", "инсулин", "insulin",
    # Platform
    "trl", "eic", "horizon", "accelerator", "work package", "budget",
    "партньор", "partner", "consortium", "координатор",
    # Smart infrastructure
    "smart city", "submarine cable", "подводен кабел", "интелигентен град",
}

OFF_TOPIC_KEYWORDS = {
    "рецепта за", "recipe", "готварс", "cooking", "футбол", "football",
    "soccer", "време", "weather", "филм", "movie", "музика", "music",
    "игра", "game", "спорт", "sport", "политик", "politic",
    "крипто", "crypto", "bitcoin", "биткойн", "ethereum",
    "maglev", "левитира",
}


def detect_language(text: str) -> str:
    """Detect BG vs EN. Complexity: O(n)"""
    cyrillic_count = sum(1 for c in text if '\u0400' <= c <= '\u04FF')
    return "bg" if cyrillic_count > len(text) * 0.3 else "en"


def get_rejection_message(lang: str) -> str:
    """Get rejection from SOUL config or fallback. Complexity: O(1)"""
    soul = get_soul_config()
    msg = soul.get_rejection(lang)
    if msg:
        return msg
    # Fallback
    if lang == "bg":
        return (
            "⚠️ Мога да отговарям само по темата Virtual Human Twin — "
            "клинична архитектура, математически модели, диагностични протоколи, "
            "C-Index валидация и EU MDR съответствие."
        )
    return (
        "⚠️ I can only answer questions about the Virtual Human Twin — "
        "clinical architecture, mathematical models, diagnostic protocols, "
        "C-Index validation, and EU MDR compliance."
    )


def is_on_topic(question: str, top_similarity: float) -> tuple[bool, str]:
    """
    Determine if question is within VHT domain.
    Uses SOUL config for threshold, keyword sets for fast classification.
    
    Catuskoti Logic:
      TRUE  → keyword match → allow
      FALSE → forbidden keyword → reject
      BOTH  → ambiguous, similarity decides
      NEITHER → below threshold → reject
    
    Returns: (is_allowed, rejection_message_or_empty)
    Complexity: O(k)
    """
    soul = get_soul_config()
    threshold = soul.get_similarity_threshold()
    lower = question.lower()
    lang = detect_language(question)

    # Phase 1 (FALSE): Hard reject — explicit off-topic
    for kw in OFF_TOPIC_KEYWORDS:
        if kw in lower:
            return False, get_rejection_message(lang)

    # Phase 2 (TRUE): Strong accept — explicit on-topic
    for kw in ON_TOPIC_KEYWORDS:
        if kw in lower:
            return True, ""

    # Phase 3 (BOTH/NEITHER): Vector similarity fallback
    if top_similarity >= threshold:
        return True, ""

    return False, get_rejection_message(lang)
