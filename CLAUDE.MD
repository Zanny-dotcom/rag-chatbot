# CLAUDE.md — rag-chatbot (Backend)

## Project
Local RAG chatbot backend that powers the chat widget on oskariozan.com.
Reads markdown notes, embeds them, retrieves relevant chunks per query, sends to Groq for the answer.

## Stack (decisions already made — do NOT suggest alternatives)
- **Language**: Python 3.11+
- **Embeddings**: `sentence-transformers` with `BAAI/bge-small-en-v1.5` (runs locally on RTX 2070)
- **Vector store**: ChromaDB (persistent, on-disk)
- **LLM**: Groq API (model: `llama-3.3-70b-versatile` or current best — verify at runtime)
- **Web framework**: FastAPI + uvicorn
- **No LangChain. No LlamaIndex.** Plain Python only. The point is to understand and own every line.

## Project Structure
```
rag-chatbot/
├── notes/              # Source markdown files (gitignored — private data)
├── chroma_db/          # Persisted vector store (gitignored)
├── src/
│   ├── ingest.py       # Read notes/, chunk, embed, write to ChromaDB
│   ├── query.py        # Given a question, return top-k relevant chunks
│   ├── chat.py         # query.py + Groq call → final answer
│   └── server.py       # FastAPI wrapping chat.py as /chat endpoint
├── .env                # GROQ_API_KEY (gitignored)
├── .env.example        # Template, committed
├── .gitignore
├── requirements.txt
└── CLAUDE.md
```

## API Contract (must match website exactly)
```
POST /chat
Request body:  { "message": "user question here" }
Response body: { "answer": "the response text", "sources": ["note1.md", "note2.md"] }
```

## Build Order (one file at a time, test each before moving on)
1. `ingest.py` — run once. Verify: chunks land in ChromaDB, can list them.
2. `query.py` — hardcode a test question. Verify: retrieved chunks look relevant. Eyeball them.
3. `chat.py` — add Groq call. Verify: get a real answer in terminal.
4. `server.py` — wrap in FastAPI. Verify: curl the endpoint, get the contract response.

Do not skip ahead. Each phase has a clear "does it work?" check.

## Chunking Strategy
Markdown-aware: split on `##` and `###` headers. If a section is huge (>1000 chars),
sub-split on paragraphs (double newlines). Preserve heading context in each chunk
(prepend the parent heading to the chunk text so retrieval has semantic anchor).

Store metadata per chunk: `{source_file, heading, chunk_index}`.

## Retrieval Settings (starting points, tune later)
- top_k = 5
- Embed query and chunks with the same model
- No reranker initially. Add one (e.g. `bge-reranker-base`) only if quality is bad.

## Groq Prompt Shape
```
System: You answer questions using ONLY the provided context from the user's notes.
        If the answer isn't in the context, say so. Cite source filenames.
User:   Context:
        ---
        {retrieved_chunks_with_source_labels}
        ---
        Question: {user_message}
```

Return both the answer text and the list of source filenames used.

## CORS
FastAPI must allow origin `https://oskariozan.com` (and `http://localhost:*` for dev).

## Owner Preferences
- First-principles code, no heavy abstractions
- Type hints where useful, not everywhere
- Comments only where they add real value
- Ask before adding new dependencies beyond the stack listed above
- This will eventually deploy to a VPS — keep it simple to run (`uvicorn src.server:app`)

## Hardware Note
Dev machine has RTX 2070. Use GPU for embedding (`device='cuda'`) during ingest for speed.
Production VPS will be CPU-only — embedding model is small enough that this is fine.
