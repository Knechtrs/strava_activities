# scripts/strava_sync.py
import os
import sys
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone


def get_user_key() -> str:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/strava_sync.py <user_key>  (e.g., raphael, lauren)")
    return sys.argv[1].strip().lower()


def env_for_user(user_key: str, suffix: str) -> str:
    return f"STRAVA_{user_key.upper()}_{suffix}"


def get_required_env(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError as e:
        raise SystemExit(f"Missing environment variable: {name}") from e


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    r = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
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
    user_key = get_user_key()

    client_id = get_required_env(env_for_user(user_key, "CLIENT_ID"))
    client_secret = get_required_env(env_for_user(user_key, "CLIENT_SECRET"))
    refresh_token = get_required_env(env_for_user(user_key, "REFRESH_TOKEN"))

    outdir = Path("data/processed") / user_key
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "activities.csv"

    token = refresh_access_token(client_id, client_secret, refresh_token)
    rows = fetch_activities(token)

    df = pd.json_normalize(rows)
    df["pulled_at_utc"] = datetime.now(timezone.utc).isoformat()
    df.to_csv(outfile, index=False)

    print(f"[{user_key}] Wrote {len(df)} activities to {outfile}")


if __name__ == "__main__":
    main()
