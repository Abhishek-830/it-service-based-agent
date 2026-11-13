from src.rag.vector_store import build_vector_store


index, chunks = build_vector_store()


print("\n========== VECTOR STORE TEST ==========")

print("FAISS Index Type:", type(index).__name__)

print("Total Stored Vectors:", index.ntotal)

print("Total Metadata Records:", len(chunks))

print("Vector Dimension:", index.d)

print("\nVector Store Test Successful!")