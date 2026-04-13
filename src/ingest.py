"""
Read markdown notes, chunk them, embed with bge-small-en-v1.5, store in ChromaDB.
Run once (or re-run to rebuild the entire collection from scratch).
"""

import os
import re
from pathlib import Path

import torch
import chromadb
from sentence_transformers import SentenceTransformer

NOTES_DIR = Path(__file__).resolve().parent.parent / "notes"
CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "notes"
CHUNK_THRESHOLD = 1500  # chars — sub-split sections larger than this


# ── Chunking ─────────────────────────────────────────────────────────

def read_notes() -> list[dict]:
    """Return list of {filename, content} for every .md in notes/."""
    files = sorted(NOTES_DIR.glob("*.md"))
    return [{"filename": f.name, "content": f.read_text(encoding="utf-8")} for f in files]


def chunk_markdown(filename: str, content: str) -> list[dict]:
    """Split a markdown file into chunks, preserving heading context."""
    lines = content.split("\n")
    chunks: list[dict] = []

    title = ""          # the # heading
    parent_heading = ""  # current ## heading
    current_heading = "" # current ## or ### heading
    section_lines: list[str] = []

    def flush():
        text = "\n".join(section_lines).strip()
        if not text:
            return
        heading_ctx = current_heading
        # if we're inside a ### under a ##, prepend the parent
        if parent_heading and current_heading != parent_heading:
            heading_ctx = f"{parent_heading}\n{current_heading}"
        # if there's a file title distinct from the section heading, prepend it
        if title and title not in heading_ctx:
            heading_ctx = f"{title}\n{heading_ctx}"

        for sub_chunk in sub_split(text):
            chunks.append({
                "source_file": filename,
                "heading": heading_ctx.strip(),
                "chunk_index": len(chunks),
                "text": f"{heading_ctx.strip()}\n\n{sub_chunk}" if heading_ctx.strip() else sub_chunk,
            })

    for line in lines:
        # detect heading level
        if line.startswith("# ") and not line.startswith("## "):
            flush()
            section_lines = []
            title = line.strip()
            current_heading = title
        elif line.startswith("## ") and not line.startswith("### "):
            flush()
            section_lines = []
            parent_heading = line.strip()
            current_heading = parent_heading
        elif line.startswith("### "):
            flush()
            section_lines = []
            current_heading = line.strip()
        else:
            section_lines.append(line)

    flush()  # last section
    return chunks


def sub_split(text: str) -> list[str]:
    """Split text on paragraph breaks if it exceeds CHUNK_THRESHOLD."""
    if len(text) <= CHUNK_THRESHOLD:
        return [text]

    paragraphs = re.split(r"\n{2,}", text)
    sub_chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # if adding this paragraph would exceed threshold, flush
        if current and current_len + len(para) > CHUNK_THRESHOLD:
            sub_chunks.append("\n\n".join(current))
            current = [para]
            current_len = len(para)
        else:
            current.append(para)
            current_len += len(para)

    if current:
        sub_chunks.append("\n\n".join(current))

    return sub_chunks


# ── Embedding & Storage ──────────────────────────────────────────────

def embed_and_store(chunks: list[dict]):
    """Embed all chunks and write to ChromaDB."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading embedding model on {device}...")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5", device=device)

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    print(f"Writing to ChromaDB at {CHROMA_DIR}...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # drop and recreate to ensure clean state on re-run
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [
        {"source_file": c["source_file"], "heading": c["heading"], "chunk_index": c["chunk_index"]}
        for c in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=[e.tolist() for e in embeddings],
        documents=texts,
        metadatas=metadatas,
    )

    return collection


# ── Main ─────────────────────────────────────────────────────────────

def main():
    notes = read_notes()
    print(f"Found {len(notes)} markdown files in {NOTES_DIR}\n")

    all_chunks: list[dict] = []
    for note in notes:
        file_chunks = chunk_markdown(note["filename"], note["content"])
        print(f"  {note['filename']}: {len(file_chunks)} chunks")
        all_chunks.extend(file_chunks)

    print(f"\nTotal chunks: {len(all_chunks)}\n")

    collection = embed_and_store(all_chunks)

    print(f"\nChromaDB collection '{COLLECTION_NAME}' count: {collection.count()}")

    # show 3 sample chunks
    print("\n-- Sample chunks ------------------------------------\n")
    samples = [all_chunks[0], all_chunks[len(all_chunks) // 2], all_chunks[-1]]
    for i, c in enumerate(samples):
        print(f"[Sample {i+1}]")
        print(f"  source_file:  {c['source_file']}")
        print(f"  heading:      {c['heading'][:80]}")
        print(f"  chunk_index:  {c['chunk_index']}")
        print(f"  text length:  {len(c['text'])} chars")
        print(f"  text preview: {c['text'][:200]}...")
        print()


if __name__ == "__main__":
    main()
