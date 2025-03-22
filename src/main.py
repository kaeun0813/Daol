import functions_framework
from flask import jsonify, request
from storage_handler import download_from_gcs, upload_to_gcs
from pdf_processor import extract_text_from_pdf, split_text
from summarizer import summarize_text

# 📌 GCS 트리거 기반 요약 (파일 업로드 시 자동 실행)
@functions_framework.cloud_event
def summarize_pdf_gcs(cloud_event):
    bucket_name = cloud_event.data["bucket"]
    file_name = cloud_event.data["name"]

    # GCS에서 PDF 다운로드
    local_pdf_path = f"/tmp/{file_name}"
    download_from_gcs(bucket_name, file_name, local_pdf_path)

    # PDF → 텍스트 변환 & Chunking
    text = extract_text_from_pdf(local_pdf_path)
    chunks = split_text(text)

    # Google Studio AI로 요약
    summarized_chunks = [summarize_text(chunk) for chunk in chunks]
    final_summary = "\n".join(summarized_chunks)

    # 요약 결과를 GCS output 폴더에 저장
    output_file = file_name.replace(".pdf", "_summary.txt")
    upload_to_gcs(bucket_name, f"output/{output_file}", final_summary)

    print(f"Summary saved: gs://{bucket_name}/output/{output_file}")
    return jsonify({"message": "Summary saved successfully"}), 200


# 📌 REST API 기반 요약 (요청 시 실행)
@functions_framework.http
def summarize_text_api(request):
    request_json = request.get_json()
    text = request_json.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    chunks = split_text(text)
    summarized_chunks = [summarize_text(chunk) for chunk in chunks]
    final_summary = "\n".join(summarized_chunks)

    return jsonify({"summary": final_summary}), 200
