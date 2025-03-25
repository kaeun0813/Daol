from google.cloud import storage

def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
    """GCS에서 PDF 다운로드"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"📥 다운로드 완료: {source_blob_name} → {destination_file_name}")

from google.cloud import storage

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """GCS에 요약 파일 업로드 (UTF-8 인코딩 명시)"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # 파일을 UTF-8로 읽기
    with open(source_file_name, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Blob에 UTF-8 인코딩된 내용 업로드
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content, content_type='text/plain; charset=UTF-8')
    
    print(f"📤 업로드 완료: {source_file_name} → {destination_blob_name}")
