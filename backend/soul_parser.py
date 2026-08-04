# ═══════════════════════════════════════════════════════════════
# AETERNA VHT — SOUL DSL Parser
# Reads .soul configuration files and extracts manifold data
# Complexity: O(n) where n = file size
# ═══════════════════════════════════════════════════════════════

import re
from pathlib import Path


class SoulManifold:
    """Parsed manifold from a .soul file."""
    
    def __init__(self, name: str):
        self.name = name
        self.properties: dict = {}
        self.entrenched: dict = {}
        self.resonances: dict = {}
        self.collapses: dict = {}
        self.pipelines: dict = {}


class SoulConfig:
    """
    Parsed SOUL configuration.
    Reads .soul files and exposes manifolds as structured data.
    """
    
    def __init__(self):
        self.manifolds: dict[str, SoulManifold] = {}
        self.raw_content: str = ""
    
    @classmethod
    def from_file(cls, path: Path) -> "SoulConfig":
        """Parse a .soul file into structured config. Complexity: O(n)"""
        config = cls()
        config.raw_content = path.read_text(encoding="utf-8")
        config._parse()
        return config
    
    def _parse(self):
        """Extract manifolds, entrenchments, and resonances."""
        lines = self.raw_content.split("\n")
        current_manifold = None
        current_entrench = None
        entrench_content = []
        brace_depth = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Skip comments and empty lines
            if stripped.startswith("//") or not stripped:
                continue
            
            # Detect manifold declaration
            manifold_match = re.match(r'manifold\s+(\w+)\s*\{', stripped)
            if manifold_match:
                name = manifold_match.group(1)
                current_manifold = SoulManifold(name)
                self.manifolds[name] = current_manifold
                brace_depth = 1
                continue
            
            if current_manifold:
                # Track brace depth
                brace_depth += stripped.count('{') - stripped.count('}')
                
                if brace_depth <= 0:
                    current_manifold = None
                    current_entrench = None
                    brace_depth = 0
                    continue
                
                # Parse resonate
                res_match = re.match(r'resonate\s+(\w+)\((.+?)\);', stripped)
                if res_match:
                    key, val = res_match.group(1), res_match.group(2)
                    current_manifold.resonances[key] = self._parse_value(val)
                    continue
                
                # Parse collapse
                col_match = re.match(r'collapse\s+(\w+)\((.+?)\);', stripped)
                if col_match:
                    key, val = col_match.group(1), col_match.group(2)
                    current_manifold.collapses[key] = self._parse_value(val)
                    continue
                
                # Parse entrench block
                ent_match = re.match(r'entrench\s+(\w+)\s*[\{\[]', stripped)
                if ent_match:
                    current_entrench = ent_match.group(1)
                    entrench_content = []
                    continue
                
                # Parse entrench items (key: value pairs)
                if current_entrench:
                    kv_match = re.match(r'(\w+):\s*(.+?);?\s*$', stripped)
                    if kv_match:
                        key, val = kv_match.group(1), kv_match.group(2)
                        if current_entrench not in current_manifold.entrenched:
                            current_manifold.entrenched[current_entrench] = {}
                        current_manifold.entrenched[current_entrench][key] = self._parse_value(val.rstrip(';'))
                    
                    # String items in lists
                    str_match = re.match(r'"(.+?)"', stripped)
                    if str_match and isinstance(current_manifold.entrenched.get(current_entrench), list):
                        current_manifold.entrenched[current_entrench].append(str_match.group(1))
                    elif str_match and current_entrench not in current_manifold.entrenched:
                        current_manifold.entrenched[current_entrench] = [str_match.group(1)]
                    
                    if ']' in stripped or ('}' in stripped and '{' not in stripped):
                        current_entrench = None
    
    @staticmethod
    def _parse_value(val: str):
        """Parse a SOUL value literal."""
        val = val.strip().strip('"').strip("'")
        # Number
        try:
            if '.' in val:
                return float(val)
            return int(val, 0)  # Supports hex (0x...)
        except (ValueError, TypeError):
            pass
        # Boolean
        if val.lower() in ('true', 'false'):
            return val.lower() == 'true'
        return val
    
    def get_system_prompt(self, lang: str = "bg") -> str:
        """Extract system prompt for given language."""
        identity = self.manifolds.get("COPILOT_IDENTITY", SoulManifold(""))
        prompts = identity.entrenched.get("SYSTEM_PROMPT", {})
        return prompts.get(lang, prompts.get("en", ""))
    
    def get_rejection(self, lang: str = "bg") -> str:
        """Extract rejection message for given language."""
        boundaries = self.manifolds.get("KNOWLEDGE_BOUNDARIES", SoulManifold(""))
        rejection = boundaries.entrenched.get("REJECTION", {})
        return rejection.get(lang, rejection.get("en", ""))
    
    def get_similarity_threshold(self) -> float:
        """Extract minimum cosine similarity threshold."""
        boundaries = self.manifolds.get("KNOWLEDGE_BOUNDARIES", SoulManifold(""))
        threshold_config = boundaries.entrenched.get("VECTOR_THRESHOLD", {})
        return float(threshold_config.get("min_cosine_similarity", 0.30))
    
    def get_top_k(self) -> int:
        """Extract top-k retrieval count."""
        boundaries = self.manifolds.get("KNOWLEDGE_BOUNDARIES", SoulManifold(""))
        threshold_config = boundaries.entrenched.get("VECTOR_THRESHOLD", {})
        return int(threshold_config.get("top_k_retrieval", 5))
    
    def get_embedding_model(self) -> str:
        """Extract embedding model name."""
        config = self.manifolds.get("EMBEDDING_CONFIG", SoulManifold(""))
        model = config.entrenched.get("MODEL", {})
        return model.get("name", "sentence-transformers/all-MiniLM-L6-v2")
    
    def get_chunk_config(self) -> dict:
        """Extract chunking configuration."""
        config = self.manifolds.get("EMBEDDING_CONFIG", SoulManifold(""))
        return config.entrenched.get("CHUNKING", {
            "chunk_size": 500,
            "chunk_overlap": 75,
        })
    
    def get_confidence_tiers(self) -> dict:
        """Extract confidence tier thresholds."""
        protocol = self.manifolds.get("RESPONSE_PROTOCOL", SoulManifold(""))
        return protocol.entrenched.get("CONFIDENCE_TIERS", {
            "HIGH": {"threshold": 0.70, "prefix": "✅"},
            "MEDIUM": {"threshold": 0.45, "prefix": "⚡"},
            "LOW": {"threshold": 0.30, "prefix": "⚠️"},
        })


# ── Quick Test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    soul_path = Path(__file__).parent / "soul" / "copilot_genesis.soul"
    if soul_path.exists():
        config = SoulConfig.from_file(soul_path)
        print(f"Parsed {len(config.manifolds)} manifolds:")
        for name, m in config.manifolds.items():
            print(f"  - {name}: {len(m.entrenched)} entrenched, {len(m.resonances)} resonances")
        print(f"\nSimilarity threshold: {config.get_similarity_threshold()}")
        print(f"Embedding model: {config.get_embedding_model()}")
        print(f"Top-K: {config.get_top_k()}")
    else:
        print(f"[ERROR] Soul file not found: {soul_path}")
