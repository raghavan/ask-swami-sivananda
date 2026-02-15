"""Shared chat logic used by both Vercel serverless function and local dev server."""

import os
from pinecone import Pinecone
from openai import OpenAI

# Initialize clients
pinecone_client = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Configuration
INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "swami-sivananda-new")
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSION = 1024
CHAT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are Swami Sivananda, a beloved spiritual teacher known for practical wisdom, compassion, and clarity.

Your communication style:
- Practical and direct, giving actionable guidance
- Warm and compassionate, addressing seekers as "dear friend", "beloved soul"
- Use simple, clear language accessible to all
- Often give step-by-step instructions
- Quote from scriptures when relevant
- Focus on ROOT CAUSES, not just symptoms
- Emphasize self-effort, practice (Abhyasa), and detachment (Vairagya)
- End responses with blessings like "Om Shanti"

Answer based on the teachings from your books below."""


def get_chat_response(question, chat_history=None):
    """Process a question through embedding -> Pinecone search -> chat completion.

    Returns dict with 'answer' and 'sources' keys.
    """
    if chat_history is None:
        chat_history = []

    # Embed question
    embedding_response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL, dimensions=EMBEDDING_DIMENSION, input=question
    )
    question_embedding = embedding_response.data[0].embedding

    # Query Pinecone
    index = pinecone_client.Index(INDEX_NAME)
    search_results = index.query(vector=question_embedding, top_k=5, include_metadata=True)

    context_texts = []
    sources = []
    for match in search_results.matches:
        context_texts.append(match.metadata.get('text', ''))
        book = match.metadata.get('book', 'Unknown')
        if book not in [s['book'] for s in sources]:
            sources.append({'book': book, 'score': round(match.score, 3)})

    context = "\n\n".join(context_texts)

    # Build messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({
        "role": "user",
        "content": f"Context from your writings:\n\n{context}\n\nQuestion: {question}\n\nAnswer as Swami Sivananda would:"
    })

    # Chat completion
    completion = openai_client.chat.completions.create(
        model=CHAT_MODEL, messages=messages, max_completion_tokens=800
    )
    answer = completion.choices[0].message.content or ""

    return {"answer": answer, "sources": sources[:3]}
