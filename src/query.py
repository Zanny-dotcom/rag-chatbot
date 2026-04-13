"""
Given a question, retrieve the top-k most relevant chunks from ChromaDB.
"""

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "notes"
TOP_K = 5

# load once at module level so callers don't pay startup cost per query
_model = SentenceTransformer("BAAI/bge-small-en-v1.5")
_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
_collection = _client.get_collection(COLLECTION_NAME)


def query(question: str, top_k: int = TOP_K) -> list[dict]:
    """Return top-k chunks most relevant to the question.

    Each result dict has: text, source_file, heading, chunk_index, distance.
    """
    embedding = _model.encode(question, normalize_embeddings=True).tolist()

    results = _collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source_file": results["metadatas"][0][i]["source_file"],
            "heading": results["metadatas"][0][i]["heading"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i],
        })

    return chunks


# ── Manual test ──────────────────────────────────────────────────────

if __name__ == "__main__":
    test_question = "How does sleep deprivation affect the brain?"
    print(f"Question: {test_question}\n")

    results = query(test_question)
    for i, r in enumerate(results):
        print(f"--- Result {i+1} (distance: {r['distance']:.4f}) ---")
        print(f"  source: {r['source_file']}")
        print(f"  heading: {r['heading'][:100]}")
        print(f"  text preview: {r['text'][:250]}...")
        print()
