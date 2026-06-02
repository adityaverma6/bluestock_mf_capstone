import requests
import pandas as pd

scheme_code = "125497"

url = f"https://api.mfapi.in/mf/{scheme_code}"

response = requests.get(url)
data = response.json()

nav_df = pd.DataFrame(data["data"])

nav_df["scheme_code"] = data["meta"]["scheme_code"]
nav_df["scheme_name"] = data["meta"]["scheme_name"]

nav_df.to_csv(
    "../data/raw/hdfc_top100_nav_history.csv",
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
    "../data/raw/top5_bluechip_nav.csv",
    index=False
)

