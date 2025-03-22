import requests
from config import API_URL, API_KEY

def summarize_text(chunk):
    """Google Studio AI API를 사용하여 텍스트 요약"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"text": chunk, "max_tokens": 500}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        data = response.json()
        return data.get("summary", "⚠️ 요약 결과 없음")
    
    except requests.exceptions.RequestException as e:
        return f"🚨 API 요청 오류: {e}"
    except ValueError:  # JSON 디코딩 오류 대비
        return "🚨 응답이 JSON 형식이 아닙니다."
