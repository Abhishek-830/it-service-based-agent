from src.rag.rag_pipeline import generate_rag_answer


query = "My laptop is not connecting to office Wi-Fi. How can I fix it?"


print("\n========== USER QUESTION ==========")

print(query)


print("\nGenerating RAG Answer...")


result = generate_rag_answer(
    query=query,
    top_k=3
)


print("\n========== AI GENERATED ANSWER ==========")

print(result["answer"])


print("\n========== SOURCE REFERENCES ==========")

for source in result["sources"]:

    print("\nSource:", source["source"])

    print("Page:", source["page_number"])

    print(
        "Similarity Score:",
        round(source["similarity_score"], 4)
    )


print("\nRAG Pipeline Test Successful!")