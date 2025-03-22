from google.cloud import storage

storage_client = storage.Client()

def download_from_gcs(bucket_name, file_name, local_path):
    """GCS에서 파일 다운로드"""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(local_path)

def upload_to_gcs(bucket_name, destination_path, content):
    """GCS에 결과 파일 업로드"""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_path)
    blob.upload_from_string(content)
