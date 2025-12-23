import google.generativeai as genai
import os
import json

def analyze_feedback_with_ai(raw_text):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Analyze the following university feedback and return ONLY a JSON object:
    Text: "{raw_text}"
    
    JSON Format:
    {{
        "category": "technical/service/staff/other",
        "severity": 1-4,
        "tone": "aggressive/neutral/polite/disappointed",
        "intent": "complaint/suggestion/praise/question"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # JSON kısmını temizleyip alıyoruz
        result = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(result)
    except:
        return None