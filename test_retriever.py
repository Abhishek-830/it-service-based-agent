from src.rag.retriever import semantic_search


query = "My laptop is unable to connect to office Wi-Fi."


print("\n========== USER QUERY ==========")

print(query)


print("\nSearching Knowledge Base...")


results = semantic_search(
    query=query,
    top_k=3
)


print("\n========== SEARCH RESULTS ==========")

for index, result in enumerate(results, start=1):

    print(f"\n--- Result {index} ---")

    print("Source:", result["source"])

    print("Page Number:", result["page_number"])

    print("Chunk ID:", result["chunk_id"])

    print(
        "Similarity Score:",
        round(result["similarity_score"], 4)
    )

    print("\nRetrieved Text:")

    print(result["text"])


print("\nSemantic Search Successful!")