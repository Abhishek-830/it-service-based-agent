from pathlib import Path
from pypdf import PdfReader

from src.config import BASE_DIR


# PDF Documents Directory
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def extract_pdf_text(pdf_path: str) -> list:

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_file}"
        )

    reader = PdfReader(str(pdf_file))

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():

            extracted_pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    return extracted_pages


def load_all_pdfs():

    documents = []

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in: {DOCUMENTS_DIR}"
        )

    for pdf_file in pdf_files:

        print(f"\nProcessing PDF: {pdf_file.name}")

        pages = extract_pdf_text(str(pdf_file))

        for page in pages:

            documents.append({
                "source": pdf_file.name,
                "page_number": page["page_number"],
                "text": page["text"]
            })

        print("Pages Extracted:", len(pages))

    return documents