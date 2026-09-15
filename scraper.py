import os
import time
import requests
import pandas as pd

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable is missing!")

CITIES = [
    # Tamil Nadu
    "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", 
    "Tiruchirappalli, Tamil Nadu", "Salem, Tamil Nadu", "Tirunelveli, Tamil Nadu",
    # Maharashtra
    "Mumbai, Maharashtra", "Pune, Maharashtra", "Nagpur, Maharashtra", 
    "Nashik, Maharashtra", "Thane, Maharashtra", "Aurangabad, Maharashtra",
    # Karnataka
    "Bangalore, Karnataka", "Mysore, Karnataka", "Hubli, Karnataka", 
    "Mangalore, Karnataka", "Belgaum, Karnataka"
]

SEARCH_QUERY = "stock market academy"

def fetch_places(query):
    url = "https://google.serper.dev/places"
    payload = {"q": query, "gl": "in"}
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("places", [])
    else:
        print(f"Failed to fetch for '{query}': {response.status_code}")
        return []

all_leads = []

for city in CITIES:
    full_query = f"{SEARCH_QUERY} in {city}"
    print(f"Scraping: {full_query}...")

    places = fetch_places(full_query)
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
    time.sleep(1)

df = pd.DataFrame(all_leads)
df.drop_duplicates(subset=["Title", "Address"], inplace=True)

output_filename = "stock_market_academies.csv"
df.to_csv(output_filename, index=False)
print(f"Completed! Extracted {len(df)} unique records saved to {output_filename}")
