from src.rag.document_loader import load_all_pdfs
from src.rag.chunker import create_document_chunks
from src.rag.embeddings import generate_embeddings


# Step 1: Load PDF
documents = load_all_pdfs()


# Step 2: Create Chunks
chunks = create_document_chunks(
    documents=documents,
    chunk_size=500,
    chunk_overlap=100
)


# Step 3: Extract chunk text
texts = [
    chunk["text"]
    for chunk in chunks
]


# Step 4: Generate Embeddings
print("\nGenerating Gemini Embeddings...")

embeddings = generate_embeddings(texts)


# Step 5: Display Results
print("\n========== EMBEDDING RESULT ==========")

print("Total Chunks:", len(chunks))

print("Embedding Shape:", embeddings.shape)

print("Embedding Dimension:", embeddings.shape[1])

print("\nFirst Chunk Embedding (First 5 Values):")

print(embeddings[0][:5])


print("\nEmbedding Generation Successful!")