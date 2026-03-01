"""Simple RAG chatbot using OpenAI.

Takes a user question, searches the corpus, and generates an answer.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

from src.corpus import Corpus

# Load .env file
load_dotenv()


def get_rag_response(question: str, corpus: Corpus) -> str:
    """Generate a response using RAG (Retrieval-Augmented Generation).

    1. Search corpus for relevant context
    2. Pass to OpenAI with the question
    3. Return answer

    Returns:
        str: The generated answer.
    """
    try:
        from openai import OpenAI
    except ImportError:
        return "Error: OpenAI package not installed. Run: pip install openai"

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY not set in .env file"

    # Step 1: Search the corpus
    results = corpus.search(question, top_k=3)

    if not results:
        return "I don't have information about that. Please contact ACC directly at info@asianchamber-hou.org or 713-782-7222."

    # Step 2: Build context from search results
    context_parts = []
    for result in results:
        context_parts.append(f"From {result['source']}:\n{result['content']}")
    context = "\n\n".join(context_parts)

    # Step 3: Create prompt with context
    system_prompt = """You are a helpful assistant for the Asian Chamber of Commerce (ACC).
You answer questions about ACC's membership, programs, benefits, and services.
Base your answers only on the provided context. If you don't have enough information, say so.
Keep answers concise and friendly. Include relevant contact info when appropriate."""

    user_prompt = f"""Context about ACC:
{context}

Question: {question}

Please answer based on the context above."""

    # Step 4: Call OpenAI
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as exc:
        return f"Error generating response: {exc}"
