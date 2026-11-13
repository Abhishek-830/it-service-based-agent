from src.rag.document_loader import load_all_pdfs


documents = load_all_pdfs()

print("\n========== PDF EXTRACTION RESULT ==========")

print("Total Pages Extracted:", len(documents))

for document in documents[:3]:

    print("\n----------------------------------")

    print("Source:", document["source"])

    print("Page Number:", document["page_number"])

    print("Extracted Text:")

    print(document["text"][:500])