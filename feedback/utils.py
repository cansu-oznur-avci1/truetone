from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

def analyze_feedback_with_ai(raw_text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("DEBUG: API KEY is missing in .env file!")
        return None
        

        # Client'ı oluştururken otomatik olarak güncel v1 sürümünü kullanır
    client = genai.Client(api_key=api_key)
        
    prompt = f"""
    Analyze and normalize this university feedback: "{raw_text}"

    1. Analyze categories: category, severity (1-4), tone, intent.
    2. Rewrite the text into a professional, polite, and constructive version. 
        - Remove any insults or aggressive language.
        - Keep the original meaning but make it sound formal (e.g., suitable for a dean's report).
    
    Return ONLY a JSON object:
    {{
        "category": "technical/service/staff/other",
        "severity": 1, 2, 3, or 4,
        "tone": "aggressive/neutral/polite/disappointed",
        "intent": "complaint/suggestion/praise/question",
        "normalized_text": "The professional version here"
    }}
    """

    try:
        # Model ismini 'models/gemini-1.5-flash' olarak yalın halde gönderiyoruz
        response = client.models.generate_content(
            model="gemini-flash-latest", 
            contents=prompt
        )   
        # Yanıt metnini temizle
        clean_json = response.text.strip().replace('```json', '').replace('```', '')
        print(f"DEBUG AI SUCCESS: {clean_json}")
        return json.loads(clean_json)
        
    except Exception as e:
        print(f"DEBUG AI ERROR: {e}")
        return None