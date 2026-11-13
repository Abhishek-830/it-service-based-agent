import json
import faiss
import numpy as np

from src.config import BASE_DIR
from src.rag.embeddings import generate_embeddings


# Vector Store Paths
VECTOR_STORE_DIR = BASE_DIR / "artifacts" / "vector_store"

INDEX_PATH = VECTOR_STORE_DIR / "faiss.index"

METADATA_PATH = VECTOR_STORE_DIR / "metadata.json"


def load_vector_store():

    if not INDEX_PATH.exists():
        raise FileNotFoundError(
            "FAISS index not found. Build the vector store first."
        )

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Metadata file not found."
        )

    # Load FAISS index
    index = faiss.read_index(str(INDEX_PATH))

    # Load metadata
    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    if index.ntotal != len(metadata):
        raise ValueError(
            "FAISS index and metadata count do not match."
        )

    return index, metadata


def semantic_search(
    query: str,
    top_k: int = 3
) -> list:

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    # Load stored vectors and metadata
    index, metadata = load_vector_store()

    # Generate query embedding
    query_embedding = generate_embeddings(
        [query],
        task_type="RETRIEVAL_QUERY"
    )

    # Normalize query vector
    faiss.normalize_L2(query_embedding)

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        min(top_k, index.ntotal)
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        result = metadata[idx].copy()

        result["similarity_score"] = float(score)

        results.append(result)

    return results