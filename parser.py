import pdfplumber
from docx import Document


def extract_pdf_text(uploaded_file):
    """
    Extract text from PDF file
    """
    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print("PDF Error:", e)

    return text


def extract_docx_text(uploaded_file):
    """
    Extract text from DOCX file
    """
    text = ""

    try:
        doc = Document(uploaded_file)

        for para in doc.paragraphs:
            text += para.text + "\n"

    except Exception as e:
        print("DOCX Error:", e)

    return text


def extract_text(uploaded_file):
    """
    Detect file type and extract text
    """

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(uploaded_file)

    elif filename.endswith(".docx"):
        return extract_docx_text(uploaded_file)

    else:
        return ""
