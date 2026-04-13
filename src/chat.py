"""
RAG chat: retrieve relevant chunks, gate on distance, call Groq for the answer.
"""

import os

from groq import Groq
from src.query import query as retrieve

DISTANCE_GATE = 0.50
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You are a concise research assistant. Answer questions based ONLY on the provided context. "
    "Keep answers to 2-3 sentences maximum — give the key takeaway, not every detail. "
    "Use plain language, not academic listing. "
    "If the context doesn't contain enough information to answer, say so. "
    "Do not make up information."
)

_groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])


def chat(question: str) -> dict:
    """Take a user question, retrieve context, call Groq, return answer + sources."""
    results = retrieve(question, top_k=5)

    # debug: print distances
    print("Distances:", [f"{r['distance']:.4f}" for r in results])

    # gate check
    if results[0]["distance"] > DISTANCE_GATE:
        print("GATE: blocked")
        return {"answer": "I don't have information on that topic in my notes.", "sources": []}

    print("GATE: passed")

    # build context block
    context_parts = []
    for i, r in enumerate(results):
        context_parts.append(f"[{i+1}] (source: {r['source_file']})\n{r['text']}")
    context = "\n\n".join(context_parts)

    user_message = f"Context:\n---\n{context}\n---\nQuestion: {question}"

    response = _groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content

    # deduplicated source filenames, preserving retrieval order
    sources = list(dict.fromkeys(r["source_file"] for r in results))

    return {"answer": answer, "sources": sources}


# ── Manual test ──────────────────────────────────────────────────────

if __name__ == "__main__":
    test_questions = [
        "What did patient SM prove about fear?",
        "How does fluoride affect the pineal gland?",
        "What is the capital of Finland?",
    ]

    for q in test_questions:
        print(f"\n{'=' * 60}")
        print(f"Q: {q}")
        print(f"{'=' * 60}")
        result = chat(q)
        print(f"\nAnswer: {result['answer']}")
        print(f"Sources: {result['sources']}")
