# ═══════════════════════════════════════════════════════════════
# AETERNA VHT Clinical Copilot — Knowledge Ingestion Pipeline
# Converts all documentation into FAISS vector embeddings
# Complexity: O(n * d) where n=chunks, d=embedding_dim(384)
# ═══════════════════════════════════════════════════════════════

import os
import json
import time
from pathlib import Path

# LangChain imports for text splitting and FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ── Configuration ─────────────────────────────────────────────
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge_base"
VECTOR_STORE_DIR = Path(__file__).parent / "vector_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # 80MB, 384-dim, multilingual
CHUNK_SIZE = 500       # characters per chunk
CHUNK_OVERLAP = 75     # overlap for context continuity


def load_documents() -> list[dict]:
    """
    Load all .md files from knowledge_base/ directory.
    Returns list of {content, metadata} dicts.
    Complexity: O(f) where f = number of files
    """
    documents = []
    
    if not KNOWLEDGE_DIR.exists():
        print(f"[ERROR] Knowledge directory not found: {KNOWLEDGE_DIR}")
        return documents
    
    for md_file in sorted(KNOWLEDGE_DIR.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            if content.strip():
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": md_file.name,
                        "size_bytes": len(content.encode("utf-8")),
                    }
                })
                print(f"  [OK] Loaded: {md_file.name} ({len(content):,} chars)")
        except Exception as e:
            print(f"  [WARN] Failed to load {md_file.name}: {e}")
    
    return documents


def chunk_documents(documents: list[dict]) -> list:
    """
    Split documents into overlapping chunks for embedding.
    Complexity: O(n) where n = total characters across all docs
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", ". ", " "],
        length_function=len,
    )
    
    all_chunks = []
    for doc in documents:
        chunks = splitter.create_documents(
            texts=[doc["content"]],
            metadatas=[doc["metadata"]],
        )
        all_chunks.extend(chunks)
    
    return all_chunks


def build_vector_store(chunks: list) -> FAISS:
    """
    Generate embeddings and build FAISS index.
    Complexity: O(n * d) where n=chunks, d=384
    """
    print(f"\n[2/3] Generating embeddings with {EMBEDDING_MODEL}...")
    print(f"      This may take 30-60 seconds on first run (downloading model)...\n")
    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
    )
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


def ingest():
    """
    Main ingestion pipeline: Load → Chunk → Embed → Store
    """
    print("=" * 60)
    print("  AETERNA VHT — Knowledge Ingestion Pipeline")
    print("=" * 60)
    
    # Step 1: Load documents
    print("\n[1/3] Loading documents from knowledge_base/...")
    documents = load_documents()
    
    if not documents:
        print("\n[FATAL] No documents found. Aborting.")
        return
    
    total_chars = sum(len(d["content"]) for d in documents)
    print(f"\n      Total: {len(documents)} documents, {total_chars:,} characters")
    
    # Step 2: Chunk
    print("\n[2/3] Splitting into chunks...")
    chunks = chunk_documents(documents)
    print(f"      Generated {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    
    # Step 3: Embed & Store
    t0 = time.time()
    vector_store = build_vector_store(chunks)
    elapsed = time.time() - t0
    
    # Save to disk
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(VECTOR_STORE_DIR))
    
    # Save metadata
    meta = {
        "documents_count": len(documents),
        "chunks_count": len(chunks),
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dim": 384,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "ingestion_time_seconds": round(elapsed, 2),
        "sources": [d["metadata"]["source"] for d in documents],
    }
    (VECTOR_STORE_DIR / "metadata.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    
    print(f"\n[3/3] Vector store saved to {VECTOR_STORE_DIR}/")
    print(f"      Embedding time: {elapsed:.1f}s")
    print(f"      Chunks indexed: {len(chunks)}")
    print("\n" + "=" * 60)
    print("  STATUS: INGESTION COMPLETE — ZERO ENTROPY")
    print("=" * 60)


if __name__ == "__main__":
    ingest()
