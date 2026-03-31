from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_claims(text: str) -> list:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a medical claim extractor. 
                Extract all health-related claims from the text.
                Return ONLY a JSON array of claims. Nothing else.
                Example: ["papaya causes miscarriage", "ghee induces labour"]"""
            },
            {
                "role": "user",
                "content": f"Extract all health claims from this text: {text}"
            }
        ]
    )
    
    result = response.choices[0].message.content
    claims = json.loads(result)
    return claims

# Test it
if __name__ == "__main__":
    test_text = "Don't eat papaya during pregnancy, it causes miscarriage. Also drink lots of ghee to make delivery easier."
    claims = extract_claims(test_text)
    print(claims)