from src.rag.document_loader import load_all_pdfs

from src.rag.chunker import create_document_chunks


# Step 1: Load PDF documents
documents = load_all_pdfs()


# Step 2: Create chunks
chunks = create_document_chunks(
    documents=documents,
    chunk_size=500,
    chunk_overlap=100
)


# Step 3: Display results
print("\n========== CHUNKING RESULT ==========")

print("Total Pages:", len(documents))

print("Total Chunks:", len(chunks))


# Display first 5 chunks
for chunk in chunks[:5]:

    print("\n--------------------------------")

    print("Chunk ID:", chunk["chunk_id"])

    print("Source:", chunk["source"])

    print("Page Number:", chunk["page_number"])

    print("Chunk Index:", chunk["chunk_index"])

    print("Text Length:", len(chunk["text"]))

    print("Text:")

    print(chunk["text"])