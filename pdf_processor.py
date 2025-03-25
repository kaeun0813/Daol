""""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image



def extract_text_from_pdf(pdf_path):
    #OCR을 사용하여 이미지 기반 PDF에서도 텍스트 추출
    doc = fitz.open(pdf_path)  # PDF 파일 열기
    text = ""

    for page in doc:
        page_text = page.get_text("text")  # 페이지에서 텍스트 추출
        if page_text.strip():
            text += page_text + "\n"  # 텍스트가 있으면 추가
        else:
            # 텍스트가 없으면 OCR 수행
            img = page.get_pixmap()  # 페이지를 이미지로 변환
            img_bytes = img.tobytes("png")  # 이미지 바이트로 변환
            image = Image.open(io.BytesIO(img_bytes))  # 이미지를 메모리에서 읽기
            ocr_text = pytesseract.image_to_string(image, lang="kor")  # 한국어 OCR 적용
            text += ocr_text + "\n"  # OCR 결과 추가

    return text.strip()  # 불필요한 공백 제거하여 반환
import pdfplumber

def extract_text_from_pdf(pdf_path):
    #PDF에서 텍스트 추출
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text if text else "📌 텍스트를 추출할 수 없습니다."


import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    #PDF에서 텍스트를 추출하고, 필요 시 OCR을 사용하여 이미지 기반 PDF도 처리
    doc = fitz.open(pdf_path)  # PDF 파일 열기
    text = ""

    for page in doc:
        page_text = page.get_text("text")  # 페이지에서 텍스트 추출
        if page_text.strip():
            text += page_text + "\n"  # 텍스트가 있으면 추가
        else:
            # 텍스트가 없으면 OCR 수행
            img = page.get_pixmap()  # 페이지를 이미지로 변환
            img_bytes = img.tobytes("png")  # PNG 형식 바이트 변환
            image = Image.open(io.BytesIO(img_bytes))  # 메모리에서 이미지 읽기
            
            # OCR 수행 (한국어 포함)
            ocr_text = pytesseract.image_to_string(image, lang="kor+eng")  
            text += ocr_text + "\n"  # OCR 결과 추가

    return text.strip()  # 불필요한 공백 제거 후 반환"""
import pdfplumber

def extract_text_from_pdf(pdf_path):
    #PDF에서 텍스트 추출
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text if text else "📌 텍스트를 추출할 수 없습니다."