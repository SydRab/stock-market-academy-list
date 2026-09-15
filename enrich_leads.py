import pandas as pd
import requests
import re

# Load original Google Maps scraper output
df = pd.read_csv("stock_market_academies.csv")

EMAIL_REGEX = r'[a-zA-Z0-9%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_REGEX = r'(?:\+91[\s-]?)?[6-9]\d{9}'

def extract_website_details(url):
    details = {
        "Scraped_Email": "",
        "Scraped_Phone": "",
        "Facebook_URL": "",
        "Instagram_URL": "",
        "LinkedIn_URL": "",
        "YouTube_URL": ""
    }
    
    if not isinstance(url, str) or not url.startswith("http"):
        return details

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, timeout=7, headers=headers)
        html = response.text

        # 1. Extract Emails
        emails = set(re.findall(EMAIL_REGEX, html))
        valid_emails = [e for e in emails if not e.endswith(('.png', '.jpg', '.jpeg', '.svg', '.webp'))]
        if valid_emails:
            details["Scraped_Email"] = valid_emails[0]

        # 2. Extract Mobile / Phone Numbers
        phones = set(re.findall(PHONE_REGEX, html))
        if phones:
            details["Scraped_Phone"] = list(phones)[0]

        # 3. Extract Social Links
        links = re.findall(r'href=["\'](https?://[^\s"\']+)["\']', html)
        for link in links:
            lower_link = link.lower()
            if "facebook.com" in lower_link and not details["Facebook_URL"]:
                details["Facebook_URL"] = link
            elif "instagram.com" in lower_link and not details["Instagram_URL"]:
                details["Instagram_URL"] = link
            elif "linkedin.com" in lower_link and not details["LinkedIn_URL"]:
                details["LinkedIn_URL"] = link
            elif "youtube.com" in lower_link and not details["YouTube_URL"]:
                details["YouTube_URL"] = link

    except Exception:
        pass

    return details

print("Enriching leads with website contact info and social profile links...")

extracted_data = df["Website"].apply(extract_website_details)
extracted_df = pd.DataFrame(list(extracted_data))
df = pd.concat([df, extracted_df], axis=1)

output_file = "stock_market_academies_fully_enriched.csv"
df.to_csv(output_file, index=False)
print(f"Enrichment complete! Saved clean contact list to {output_file}")
