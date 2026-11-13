import json
import faiss
import numpy as np

from pathlib import Path

from src.config import BASE_DIR
from src.rag.document_loader import load_all_pdfs
from src.rag.chunker import create_document_chunks
from src.rag.embeddings import generate_embeddings


# Vector Store Directory
VECTOR_STORE_DIR = BASE_DIR / "artifacts" / "vector_store"

VECTOR_STORE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# File Paths
INDEX_PATH = VECTOR_STORE_DIR / "faiss.index"

METADATA_PATH = VECTOR_STORE_DIR / "metadata.json"


# Embedding Dimension
EMBEDDING_DIMENSION = 768


def build_vector_store():

    print("\nLoading PDF Documents...")

    documents = load_all_pdfs()

    print("\nCreating Text Chunks...")

    chunks = create_document_chunks(
        documents=documents,
        chunk_size=500,
        chunk_overlap=100
    )

    if not chunks:
        raise ValueError("No text chunks available.")

    print("\nGenerating Embeddings...")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(texts)

    if embeddings.shape[1] != EMBEDDING_DIMENSION:
        raise ValueError("Unexpected embedding dimension.")

    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings)

    print("\nCreating FAISS Index...")

    index = faiss.IndexFlatIP(
        EMBEDDING_DIMENSION
    )

    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    # Save chunk metadata
    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n========== VECTOR STORE RESULT ==========")

    print("Total Vectors:", index.ntotal)

    print("Vector Dimension:", index.d)

    print("FAISS Index Saved:", INDEX_PATH)

    print("Metadata Saved:", METADATA_PATH)

    return index, chunks


if __name__ == "__main__":

    build_vector_store()