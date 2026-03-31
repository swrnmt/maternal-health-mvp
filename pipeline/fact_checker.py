from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def fact_check(claims: list) -> list:
    results = []
    
    for claim in claims:
        search = tavily.search(
            query=f"maternal health pregnancy {claim} medical evidence",
            max_results=3,
            include_domains=["who.int", "ncbi.nlm.nih.gov", "mohfw.gov.in", "nhp.gov.in", "mayoclinic.org"]
        )
        
        evidence = []
        for r in search["results"]:
            evidence.append({
                "content": r["content"],
                "url": r["url"],
                "title": r["title"]
            })
        
        results.append({
            "claim": claim,
            "evidence": evidence
        })
    
    return results

# Test it
if __name__ == "__main__":
    test_claims = ["papaya causes miscarriage", "ghee makes delivery easier"]
    results = fact_check(test_claims)
    for r in results:
        print(f"\nCLAIM: {r['claim']}")
        print(f"SOURCES FOUND: {len(r['evidence'])}")
        for e in r['evidence']:
            print(f"  → {e['title']} ({e['url']})")