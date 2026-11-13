def split_text_into_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list:

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    text = text.strip()

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def create_document_chunks(
    documents: list,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list:

    all_chunks = []

    for document in documents:

        text_chunks = split_text_into_chunks(
            text=document["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for index, chunk_text in enumerate(text_chunks):

            all_chunks.append({

                "chunk_id": len(all_chunks) + 1,

                "source": document["source"],

                "page_number": document["page_number"],

                "chunk_index": index + 1,

                "text": chunk_text

            })

    return all_chunks