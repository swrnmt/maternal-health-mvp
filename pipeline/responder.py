from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(fact_check_results: list) -> dict:
    
    # Format evidence for the prompt
    evidence_text = ""
    for item in fact_check_results:
        evidence_text += f"\nCLAIM: {item['claim']}\n"
        for e in item['evidence']:
            evidence_text += f"SOURCE: {e['title']} ({e['url']})\nCONTENT: {e['content'][:300]}\n"
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a maternal health fact-checker for rural Indian women.
                
Using ONLY the provided evidence, analyze each claim and return a JSON response.
NEVER use knowledge outside the provided sources.
If evidence is weak or missing, say "insufficient verified medical evidence".

Return ONLY this JSON format, nothing else:
{
  "claims": ["claim 1", "claim 2"],
  "verdict": "TRUE/FALSE/PARTIALLY TRUE/UNVERIFIED",
  "severity": "DANGEROUS/HARMFUL/BENIGN",
  "confidence": 0.0 to 1.0,
  "response": "Simple, respectful explanation with inline citations like [Source: url]",
  "cited_sources": ["url1", "url2"]
}

Severity guide:
- DANGEROUS: could cause direct physical harm
- HARMFUL: medically wrong but less direct danger  
- BENIGN: cultural belief, not medically dangerous

Confidence guide:
- 0.85-1.0: strong evidence found
- 0.60-0.84: some evidence, uncertain
- below 0.60: insufficient evidence"""
            },
            {
                "role": "user",
                "content": f"Analyze these claims using ONLY this evidence:\n{evidence_text}"
            }
        ]
    )
    
    result = response.choices[0].message.content
    # Clean any markdown if present
    result = result.replace("```json", "").replace("```", "").strip()
    return json.loads(result)

# Test it
if __name__ == "__main__":
    # Simulated fact check results
    test_results = [
        {
            "claim": "papaya causes miscarriage",
            "evidence": [
                {
                    "title": "Dietary taboos in pregnancy",
                    "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8718855/",
                    "content": "Unripe papaya contains latex which may stimulate uterine contractions. Ripe papaya is generally considered safe in moderate amounts during pregnancy."
                }
            ]
        }
    ]
    
    result = generate_response(test_results)
    print(json.dumps(result, indent=2))