import os
import time
import requests
import pandas as pd

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable is missing!")

# Metro zones + core hubs across Tamil Nadu & Maharashtra
CITIES = [
    # Tamil Nadu
    "Chennai, Tamil Nadu", "Anna Nagar Chennai, Tamil Nadu", "T Nagar Chennai, Tamil Nadu",
    "Tambaram Chennai, Tamil Nadu", "Velachery Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu",
    "Madurai, Tamil Nadu", "Tiruchirappalli, Tamil Nadu", "Salem, Tamil Nadu",
    "Tirunelveli, Tamil Nadu", "Erode, Tamil Nadu", "Tiruppur, Tamil Nadu",
    # Maharashtra
    "Mumbai, Maharashtra", "Andheri Mumbai, Maharashtra", "Borivali Mumbai, Maharashtra",
    "Dadar Mumbai, Maharashtra", "Thane, Maharashtra", "Navi Mumbai, Maharashtra",
    "Pune, Maharashtra", "Kothrud Pune, Maharashtra", "Viman Nagar Pune, Maharashtra",
    "Nagpur, Maharashtra", "Nashik, Maharashtra", "Chhatrapati Sambhajinagar, Maharashtra",
    "Kolhapur, Maharashtra", "Solapur, Maharashtra"
]

SEARCH_QUERIES = [
    "stock market academy", "share market training classes",
    "stock trading institute", "options trading academy", "share market class"
]

def fetch_places(query, page=1):
    url = "https://google.serper.dev/places"
    payload = {"q": query, "gl": "in", "page": page}
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    
    try:
        # Added timeout=5 to prevent hanging HTTP connections
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json().get("places", [])
        return []
    except Exception as e:
        print(f"Skipping '{query}' due to error: {e}")
        return []

all_leads = []

for city in CITIES:
    for base_query in SEARCH_QUERIES:
        full_query = f"{base_query} in {city}"
        
        for page in range(1, 3):
            print(f"Scraping: {full_query} (Page {page})...")
            places = fetch_places(full_query, page=page)
            
            if not places:
                break
                
            for p in places:
                all_leads.append({
                    "City": city.split(",")[0],
                    "State": city.split(",")[1].strip(),
                    "Title": p.get("title", ""),
                    "Address": p.get("address", ""),
                    "Phone": p.get("phoneNumber", ""),
                    "Website": p.get("website", ""),
                    "Rating": p.get("rating", ""),
                    "Rating_Count": p.get("ratingCount", ""),
                    "Category": p.get("category", "")
                })
            time.sleep(0.05)

df = pd.DataFrame(all_leads)
if not df.empty:
    df.drop_duplicates(subset=["Title", "Address"], inplace=True)
    df.to_csv("stock_market_academies.csv", index=False)
    print(f"Completed! Extracted {len(df)} unique records.")
else:
    print("No records extracted.")
