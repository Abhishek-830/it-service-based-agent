from groq import Groq

from src.config import GROQ_API_KEY
from src.agent.llm_client import MODEL_NAME
from src.rag.retriever import semantic_search


# Initialize Groq Client
client = Groq(
    api_key=GROQ_API_KEY
)


def generate_rag_answer(
    query: str,
    top_k: int = 3
) -> dict:
    """
    Retrieve relevant documents and generate
    an answer using Groq LLM.
    """

    # Step 1: Retrieve relevant chunks
    retrieved_chunks = semantic_search(
        query=query,
        top_k=top_k
    )

    if not retrieved_chunks:
        return {
            "answer": "No relevant information found in the knowledge base.",
            "sources": []
        }

    # Step 2: Prepare context
    context_parts = []

    sources = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
Source: {chunk['source']}
Page: {chunk['page_number']}
Content:
{chunk['text']}
"""
        )

        sources.append({
            "source": chunk["source"],
            "page_number": chunk["page_number"],
            "similarity_score": chunk["similarity_score"]
        })

    context = "\n\n".join(context_parts)

    # Step 3: Prepare system prompt
    system_prompt = """
You are an IT Service Desk AI Assistant.

Answer the user's question using ONLY the
provided knowledge base context.

Rules:
1. Do not invent technical information.
2. If the context does not contain the answer,
   clearly say that the knowledge base does not
   provide enough information.
3. Give practical and easy-to-follow steps.
4. Do not expose confidential information.
5. Keep the answer professional and clear.
6. Mention relevant source document and page number
   when possible.
"""

    # Step 4: Generate answer using Groq
    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""
Knowledge Base Context:

{context}

User Question:

{query}

Provide an answer based on the knowledge base.
"""
            }
        ],

        temperature=0.2,

        max_completion_tokens=1000
    )

    answer = response.choices[0].message.content

    # Step 5: Return answer and sources
    return {
        "answer": answer,
        "sources": sources
    }