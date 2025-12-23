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
        
    try:
        # Client'ı oluştururken otomatik olarak güncel v1 sürümünü kullanır
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Analyze the university feedback: "{raw_text}"
        Return ONLY a JSON object with these EXACT lowercase keys:
        - "category": choose from ["technical", "service", "staff", "other"]
        - "severity": choose integer from [1, 2, 3, 4]
        - "tone": choose from ["aggressive", "neutral", "polite", "disappointed"]
        - "intent": choose from ["complaint", "suggestion", "praise", "question"]
        """

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