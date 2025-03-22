import fitz  # PyMuPDF
import textwrap

def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트 추출"""
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])

def split_text(text, max_length=3000):
    """긴 텍스트를 일정 크기로 분할"""
    return textwrap.wrap(text, width=max_length, break_long_words=False)
