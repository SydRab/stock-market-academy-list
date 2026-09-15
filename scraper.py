import os
import time
import requests
import pandas as pd

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY environment variable is missing!")

# High-priority Metro zones + Key Tier-1/Tier-2 hubs (excluding Karnataka/Bangalore)
CITIES = [
    # Tamil Nadu - Core Hubs & Metro Zones
    "Chennai, Tamil Nadu",
    "Anna Nagar Chennai, Tamil Nadu",
    "T Nagar Chennai, Tamil Nadu",
    "Tambaram Chennai, Tamil Nadu",
    "Velachery Chennai, Tamil Nadu",
    "Coimbatore, Tamil Nadu",
    "Madurai, Tamil Nadu",
    "Tiruchirappalli, Tamil Nadu",
    "Salem, Tamil Nadu",
    "Tirunelveli, Tamil Nadu",
    "Erode, Tamil Nadu",
    "Tiruppur, Tamil Nadu",

    # Maharashtra - Core Hubs & Metro Zones
    "Mumbai, Maharashtra",
    "Andheri Mumbai, Maharashtra",
    "Borivali Mumbai, Maharashtra",
    "Dadar Mumbai, Maharashtra",
    "Thane, Maharashtra",
    "Navi Mumbai, Maharashtra",
    "Pune, Maharashtra",
    "Kothrud Pune, Maharashtra",
    "Viman Nagar Pune, Maharashtra",
    "Nagpur, Maharashtra",
    "Nashik, Maharashtra",
    "Chhatrapati Sambhajinagar, Maharashtra",
    "Kolhapur, Maharashtra",
    "Solapur, Maharashtra"
]

# Diverse keywords to uncover different categorizations
SEARCH_QUERIES = [
    "stock market academy",
    "share market training classes",
    "stock trading institute",
    "options trading academy",
    "share market class"
]

def fetch_places(query, page=1):
    url = "https://google.serper.dev/places"
    payload = {
        "q": query,
        "gl": "in",
        "page": page
    }
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("places", [])
        else:
            print(f"Failed '{query}' (Page {page}): Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching '{query}': {e}")
        return []

all_leads = []

for city in CITIES:
    for base_query in SEARCH_QUERIES:
        full_query = f"{base_query} in {city}"
        
        # Paginate through 2 pages per query (up to 40 results per combination)
        for page in range(1, 3):
            print(f"Scraping: {full_query} (Page {page})...")
            places = fetch_places(full_query, page=page)
            
            if not places:
                break  # Stop paginating if no results return for page 2
                
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
            time.sleep(0.5)

# Deduplicate based on Title & Address combination
df = pd.DataFrame(all_leads)
if not df.empty:
    df.drop_duplicates(subset=["Title", "Address"], inplace=True)
    output_filename = "stock_market_academies.csv"
    df.to_csv(output_filename, index=False)
    print(f"Completed! Extracted {len(df)} unique records saved to {output_filename}")
else:
    print("No records extracted.")
