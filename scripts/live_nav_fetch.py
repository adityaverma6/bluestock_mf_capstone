import requests
import pandas as pd
import os
import time



bluechip_schemes = {
    "SBI Bluechip": "119551",
    "ICICI Bluechip": "120503",
    "Nippon Large Cap": "118632",
    "Axis Bluechip": "119092",
    "Kotak Bluechip": "120841"
}

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

for fund_name, code in bluechip_schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        nav_data = pd.DataFrame(resp.json()["data"])
        nav_data["scheme_code"] = code
        nav_data["fund_name"] = fund_name

        safe_name = fund_name.lower().replace(" ", "_")
        filepath = os.path.join(RAW_DIR, f"{safe_name}_nav.csv")
        nav_data.to_csv(filepath, index=False)
        print(f"[OK] {fund_name} - {len(nav_data)} rows -> {filepath}")
        time.sleep(0.5)
    except Exception as e:
        print(f"[FAIL] {fund_name}: {e}")

print()


scheme_code = "125497"

url = f"https://api.mfapi.in/mf/{scheme_code}"

response = requests.get(url)
data = response.json()

nav_df = pd.DataFrame(data["data"])

nav_df["scheme_code"] = data["meta"]["scheme_code"]
nav_df["scheme_name"] = data["meta"]["scheme_name"]

nav_df.to_csv(
    "../data/processed/hdfc_top100_nav_history.csv",
    index=False
)




schemes = {
    "SBI Bluechip": "119551",
    "ICICI Bluechip": "120503",
    "Nippon Large Cap": "118632",
    "Axis Bluechip": "119092",
    "Kotak Bluechip": "120841"
}

all_nav = []

for fund_name, scheme_code in schemes.items():

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data["data"])

        df["scheme_code"] = scheme_code
        df["fund_name"] = fund_name

        all_nav.append(df)

        print(f"Downloaded {fund_name}")

    except Exception as e:
        print(f"Failed for {fund_name}: {e}")

combined_nav = pd.concat(all_nav, ignore_index=True)

combined_nav.to_csv(
    "../data/processed/top5_bluechip_nav.csv",
    index=False
)
