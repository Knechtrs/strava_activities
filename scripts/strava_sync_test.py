# scripts/strava_sync_test.py
import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

def main():
    user_key = "raphael"
    
    # Create mock data instead of calling Strava API
    mock_data = {
        "id": [1, 2, 3, 4, 5],
        "sport_type": ["Run", "Ride", "Run", "WeightTraining", "Swim"],
        "distance": [5000, 15000, 3000, 0, 2000],
        "moving_time": [1800, 3600, 1200, 600, 900],
        "elapsed_time": [2000, 3800, 1300, 700, 1000],
        "start_date_local": [
            "2026-05-11T08:00:00Z",
            "2026-05-10T09:30:00Z",
            "2026-05-09T07:15:00Z",
            "2026-05-08T18:00:00Z",
            "2026-05-07T06:45:00Z"
        ]
    }
    
    outdir = Path("data/processed") / user_key
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "activities.csv"

    df = pd.DataFrame(mock_data)
    df["pulled_at_utc"] = datetime.now(timezone.utc).isoformat()
    df.to_csv(outfile, index=False)

    print(f"[{user_key}] Wrote {len(df)} mock activities to {outfile}")

if __name__ == "__main__":
    main()