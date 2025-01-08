"""
Module to handle Text Extracting logic
"""

import textract
from docx import Document
from pdfminer.high_level import extract_text as extract_pdf_text
from pdfminer.pdfparser import PDFSyntaxError

from server.exception import UnreadableCVError


def parse_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        txt = extract_pdf_text(file_path).strip()
        if not txt:
            raise UnreadableCVError()
        return txt
    except FileNotFoundError:
        print("File not found or path is incorrect")
        raise
    except PDFSyntaxError:
        print("Not a valid PDF file")
        raise


def parse_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = Document(file_path)
        txt = "\n".join(
            [paragraph.text for paragraph in doc.paragraphs]).strip()
        if not txt:
            raise UnreadableCVError()
        return txt
    except FileNotFoundError:
        print("File not found or path is incorrect")
        raise
    except Exception as e:
        print("Error parsing DOCX file:", e)
        raise


def parse_doc(file_path: str) -> str:
    """Extract text from a DOC file."""
    try:
        txt = textract.process(file_path).decode("utf-8").strip()
        if not txt:
            raise UnreadableCVError()
        return txt
    except FileNotFoundError:
        print("File not found or path is incorrect")
        raise
    except Exception as e:
        print("Error parsing DOC file:", e)
        raise


def extract_text(file_path: str) -> str:
    """Extract text from a file based on its extension."""
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    elif file_path.endswith(".doc"):
        return parse_doc(file_path)
    else:
        raise ValueError("Unsupported file format")
