
from pypdf import PdfReader


def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):
        content = uploaded_file.getvalue()
        return content.decode("utf-8", errors="replace")

    if filename.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    raise ValueError("Only PDF and TXT files are supported.")
