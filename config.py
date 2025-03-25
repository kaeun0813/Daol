import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
