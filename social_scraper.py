import os
import time
import requests
import pandas as pd
import re

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

LOCATIONS = [
    "Tamil Nadu", "Chennai", "Coimbatore", "Madurai",
    "Maharashtra", "Mumbai", "Pune", "Nagpur"
]

PLATFORMS = [
    {"name": "Facebook", "site": "site:facebook.com"},
    {"name": "Instagram", "site": "site:instagram.com"}
]

PHONE_REGEX = r'(?:\+91[\s-]?)?[6-9]\d{9}'
EMAIL_REGEX = r'[a-zA-Z0-9%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def search_social(query):
    url = "https://google.serper.dev/search"
    payload = {"q": query, "gl": "in", "num": 20}
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=5)
        return res.json().get("organic", []) if res.status_code == 200 else []
    except Exception:
        return []

social_leads = []

for platform in PLATFORMS:
    for loc in LOCATIONS:
        query = f'{platform["site"]} "stock market academy" {loc}'
        print(f"Searching: {query}...")
        
        results = search_social(query)
        for r in results:
            snippet = r.get("snippet", "")
            
            phones = re.findall(PHONE_REGEX, snippet)
            emails = re.findall(EMAIL_REGEX, snippet)
            
            social_leads.append({
                "Platform": platform["name"],
                "Location": loc,
                "Title": r.get("title", ""),
                "URL": r.get("link", ""),
                "Snippet": snippet,
                "Extracted_Phone": phones[0] if phones else "",
                "Extracted_Email": emails[0] if emails else ""
            })
        time.sleep(0.1)

df = pd.DataFrame(social_leads)
if not df.empty:
    df.drop_duplicates(subset=["URL"], inplace=True)
    df.to_csv("social_stock_market_academies.csv", index=False)
    print(f"Saved {len(df)} social leads to social_stock_market_academies.csv")
else:
    print("No social leads extracted.")
