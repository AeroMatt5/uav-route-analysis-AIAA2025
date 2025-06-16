import requests
import pandas as pd
import time
from datetime import datetime

# Bay Area bounding box
LAT_MIN = 37.0
LAT_MAX = 38.5
LON_MIN = -123.0
LON_MAX = -121.5

INTERVAL = 30  # seconds
OUTFILE = "bay_area_flight_log.csv"

columns = [
    'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
    'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity',
    'heading', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source'
]

def fetch_snapshot():
    url = "https://opensky-network.org/api/states/all"
    params = {
        'lamin': LAT_MIN,
        'lamax': LAT_MAX,
        'lomin': LON_MIN,
        'lomax': LON_MAX
    }
    try:
        response = requests.get(
    url,
    params=params,
    timeout=10
)


        data = response.json()
        rows = data.get("states", [])
        ts = data.get("time", int(time.time()))
        df = pd.DataFrame(rows, columns=columns)
        df["timestamp"] = ts
        return df
    except Exception as e:
        print(f"[{datetime.now()}] Error: {e}")
        return pd.DataFrame(columns=columns + ["timestamp"])

def run_logger():
    print(f"Starting flight logging every {INTERVAL}s...")
    try:
        while True:
            df = fetch_snapshot()
            if not df.empty:
                df.to_csv(OUTFILE, mode='a', header=not pd.io.common.file_exists(OUTFILE), index=False)
                print(f"[{datetime.now()}] Logged {len(df)} rows")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nLogging stopped manually.")

if __name__ == "__main__":
    run_logger()
