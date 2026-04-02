import re

def preprocess_input(text: str) -> str:
    text = text.strip()
    text = re.sub(r'[^\w\s\.\,\?\!\-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def preprocess_claims(claims: list) -> list:
    claims = list(set(claims))
    claims = [c for c in claims if len(c.strip()) > 0]
    claims = [c.strip() for c in claims]
    return claims