import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

def summarize_text(text):
    """Gemini API를 사용해 텍스트 요약"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"보험 약관을 이해하기 쉽게 요약해줘:\n\n{text}"
    
    response = model.generate_content(prompt)
    return response.text
