"""
RAG chat: retrieve relevant chunks, gate on distance, call Groq for the answer.
"""

import logging
import os

from groq import Groq

from src.query import query as retrieve

logger = logging.getLogger(__name__)

DISTANCE_GATE = 0.50
MODEL = "llama-3.3-70b-versatile"
GROQ_TIMEOUT_SECONDS = 15.0

SYSTEM_PROMPT = (
    "You are a concise research assistant. Answer questions based ONLY on the provided context. "
    "Maximum 2 short sentences in plain language. No jargon, no study names, no technical terms. "
    "Explain it like you're texting a friend. "
    "If the context doesn't contain enough information to answer, say so. "
    "Do not make up information."
)

if "GROQ_API_KEY" not in os.environ:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")

_groq_client = Groq(api_key=os.environ["GROQ_API_KEY"], timeout=GROQ_TIMEOUT_SECONDS)


def chat(question: str) -> dict:
    """Take a user question, retrieve context, call Groq, return answer + sources."""
    results = retrieve(question, top_k=5)

    distances = [round(r["distance"], 4) for r in results]
    logger.info("retrieved %d chunks, distances=%s", len(results), distances)

    if results[0]["distance"] > DISTANCE_GATE:
        logger.info("gate blocked: top distance %.4f > %.2f", results[0]["distance"], DISTANCE_GATE)
        return {"answer": "I don't have information on that topic in my notes.", "sources": []}

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
    sources = list(dict.fromkeys(r["source_file"] for r in results))

    logger.info("answered with %d unique sources", len(sources))
    return {"answer": answer, "sources": sources}


# ── Manual test ──────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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
