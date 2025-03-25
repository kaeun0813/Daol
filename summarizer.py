import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

def summarize_text(text):
    """Gemini API를 사용해 텍스트 요약"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""
    아래의 보험 약관을 읽고, 중요한 내용을 간결하고 이해하기 쉽게 요약해 주세요.
    약관에서 핵심적인 조항과 유의사항을 강조하고, 어려운 용어나 복잡한 부분은 간단한 언어로 설명해주세요.
    영어는 사용하지 말고, 한국어만 사용하세요.
    
    텍스트:
    {text}
    """
    
    response = model.generate_content(prompt)
    return response.text
