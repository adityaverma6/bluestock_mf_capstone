"""Download current NAV history for the configured mutual-fund schemes."""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
API_URL = "https://api.mfapi.in/mf/{scheme_code}"
REQUEST_TIMEOUT_SECONDS = 30
LOGGER = logging.getLogger(__name__)

BLUECHIP_SCHEMES = {
    "SBI Bluechip": "119551",
    "ICICI Bluechip": "120503",
    "Nippon Large Cap": "118632",
    "Axis Bluechip": "119092",
    "Kotak Bluechip": "120841",
}


def fetch_scheme(scheme_code: str) -> dict[str, Any]:
    """Fetch and validate one scheme response from the MF API."""
    response = requests.get(
        API_URL.format(scheme_code=scheme_code),
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("data"):
        raise ValueError(f"No NAV records returned for scheme {scheme_code}")
    return payload


def safe_filename(name: str) -> str:
    """Convert a fund name into a stable lowercase filename stem."""
    return re.sub(r"[^a-z0-9]+", "_", name.casefold()).strip("_")


def download_nav_data(
    schemes: dict[str, str] = BLUECHIP_SCHEMES,
    delay_seconds: float = 0.5,
) -> pd.DataFrame:
    """Download individual and combined NAV files for configured schemes."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    frames: list[pd.DataFrame] = []

    for fund_name, scheme_code in schemes.items():
        payload = fetch_scheme(scheme_code)
        nav = pd.DataFrame(payload["data"])
        nav["scheme_code"] = scheme_code
        nav["fund_name"] = fund_name
        nav.to_csv(RAW_DATA_DIR / f"{safe_filename(fund_name)}_nav.csv", index=False)
        frames.append(nav)
        LOGGER.info("Downloaded %s NAV rows for %s", len(nav), fund_name)
        time.sleep(delay_seconds)

    combined = pd.concat(frames, ignore_index=True)
    combined.to_csv(PROCESSED_DATA_DIR / "top5_bluechip_nav.csv", index=False)
    return combined


def main() -> None:
    """Download NAV history for the configured blue-chip schemes."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    download_nav_data()


if __name__ == "__main__":
    main()
