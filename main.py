import os
import sys
import functions_framework
from flask import Flask, request
from dotenv import load_dotenv
from storage_handler import download_from_gcs, upload_to_gcs
from pdf_processor import extract_text_from_pdf
from summarizer import summarize_text

# 환경 변수 로드
load_dotenv()
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

# Flask 앱 생성 (API 엔드포인트)
app = Flask(__name__)

# 📌 **1. GCS 트리거 (Cloud Function)**
@functions_framework.cloud_event
def process_pdf_trigger(cloud_event):
    """GCS에 PDF 업로드 시 자동 실행되는 Cloud Function"""
    data = cloud_event.data
    file_name = data["name"]

    if not file_name.endswith(".pdf"):
        print(f"📌 무시: PDF가 아님 → {file_name}")
        return

    print(f"📥 GCS에서 PDF 감지: {file_name}")

    # GCS에서 PDF 다운로드
    local_pdf_path = f"/tmp/{file_name}"
    download_from_gcs(GCS_BUCKET_NAME, file_name, local_pdf_path)

    # PDF에서 텍스트 추출 및 요약
    process_and_upload_summary(local_pdf_path)

# 📌 **2. Flask API 엔드포인트**
@app.route('/process_pdf', methods=['POST'])
def process_pdf_api():
    """로컬 API 엔드포인트 - 파일 업로드하여 처리"""
    file = request.files['file']
    
    temp_file_path = f"/tmp/{file.filename}"
    file.save(temp_file_path)

    # PDF 처리 및 요약
    process_and_upload_summary(temp_file_path)

    return "✅ 요약이 완료되었습니다! GCS에 업로드되었습니다."

# 📌 **3. 공통 로직 (GCS 트리거 & 로컬 실행에서 사용)**
def process_and_upload_summary(pdf_path):
    """PDF를 처리하고 요약 후 GCS에 업로드"""
    print(f"📜 PDF에서 텍스트 추출 중: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    print("🤖 Gemini 모델로 요약 중...")
    summary = summarize_text(text)

    # 요약문 저장
    summary_file_path = pdf_path.replace(".pdf", "_summary.txt")
    with open(summary_file_path, "w", encoding="utf-8") as summary_file:
        summary_file.write(summary)

    # GCS 업로드
    summary_gcs_path = f"summaries/{os.path.basename(summary_file_path)}"
    upload_to_gcs(GCS_BUCKET_NAME, summary_file_path, summary_gcs_path)

    print(f"✅ 요약 완료! GCS 저장 위치: {summary_gcs_path}")

# 📌 **4. 로컬 실행**
if __name__ == "__main__":
    if len(sys.argv) == 2:
        process_and_upload_summary(sys.argv[1])
    else:
        print("🚀 서버 시작: http://localhost:8080")
        app.run(host="0.0.0.0", port=8080)
