# scripts/strava_sync.py
import os
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]

OUTDIR = Path("data/processed")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "activities.csv"

def refresh_access_token() -> str:
    r = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    r.raise_for_status()
    payload = r.json()
    # Do NOT print tokens (avoid leaking in logs)
    return payload["access_token"]

def fetch_activities(access_token: str, per_page: int = 200, max_pages: int = 20):
    headers = {"Authorization": f"Bearer {access_token}"}
    all_rows = []
    for page in range(1, max_pages + 1):
        r = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers=headers,
            params={"per_page": per_page, "page": page},
            timeout=30,
        )
        r.raise_for_status()
        rows = r.json()
        if not rows:
            break
        all_rows.extend(rows)
    return all_rows

def main():
    token = refresh_access_token()
    rows = fetch_activities(token)
    df = pd.json_normalize(rows)
    df["pulled_at_utc"] = datetime.now(timezone.utc).isoformat()
    df.to_csv(OUTFILE, index=False)
    print(f"Wrote {len(df)} activities to {OUTFILE}")

if __name__ == "__main__":
    main()
