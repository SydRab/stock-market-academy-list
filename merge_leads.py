import pandas as pd
import re

def clean_phone(phone):
    if not isinstance(phone, str):
        return ""
    digits = re.sub(r'\D', '', phone)
    return digits[-10:] if len(digits) >= 10 else ""

try:
    maps_df = pd.read_csv("stock_market_academies_fully_enriched.csv")
except Exception:
    maps_df = pd.DataFrame()

try:
    social_df = pd.read_csv("social_stock_market_academies.csv")
except Exception:
    social_df = pd.DataFrame()

if maps_df.empty and social_df.empty:
    print("No CSV files found to merge.")
    exit()

# Normalize phone numbers for matching
if not maps_df.empty and "Phone" in maps_df.columns:
    maps_df["clean_phone"] = maps_df["Phone"].apply(clean_phone)
elif not maps_df.empty:
    maps_df["clean_phone"] = ""

if not social_df.empty and "Extracted_Phone" in social_df.columns:
    social_df["clean_phone"] = social_df["Extracted_Phone"].apply(clean_phone)
elif not social_df.empty:
    social_df["clean_phone"] = ""

combined_df = pd.concat([maps_df, social_df], ignore_index=True)

# Deduplicate by phone number first
has_phone = combined_df[combined_df["clean_phone"] != ""].drop_duplicates(subset=["clean_phone"])
no_phone = combined_df[combined_df["clean_phone"] == ""]

final_df = pd.concat([has_phone, no_phone], ignore_index=True)

# Clean up helper column and export master CSV
final_df.drop(columns=["clean_phone"], inplace=True, errors="ignore")
final_df.to_csv("master_stock_market_leads.csv", index=False)
print(f"Master lead list generated with {len(final_df)} unique records!")
