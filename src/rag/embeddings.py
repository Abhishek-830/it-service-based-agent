import numpy as np

from google import genai
from google.genai import types

from src.config import GOOGLE_API_KEY


# Gemini Embedding Configuration
MODEL_NAME = "gemini-embedding-001"

EMBEDDING_DIMENSION = 768


# Initialize Gemini Client
client = genai.Client(
    api_key=GOOGLE_API_KEY
)


def generate_embeddings(
    texts: list,
    task_type: str = "RETRIEVAL_DOCUMENT"
) -> np.ndarray:
    """
    Generate embeddings for a list of text chunks.
    """

    if not texts:
        raise ValueError("Text list cannot be empty.")

    response = client.models.embed_content(

        model=MODEL_NAME,

        contents=texts,

        config=types.EmbedContentConfig(

            task_type=task_type,

            output_dimensionality=EMBEDDING_DIMENSION

        )
    )

    embeddings = [
        embedding.values
        for embedding in response.embeddings
    ]

    return np.array(
        embeddings,
        dtype="float32"
    )