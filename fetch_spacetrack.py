import os
import json
import requests
from pathlib import Path

SPACE_TRACK_USER = os.environ["SPACE_TRACK_USER"]
SPACE_TRACK_PASS = os.environ["SPACE_TRACK_PASS"]

LOGIN_URL = "https://www.space-track.org/ajaxauth/login"
QUERY_URL = (
    "https://www.space-track.org/basicspacedata/query"
    "/class/gp"
    "/decay_date/null-val"
    "/epoch/>now-30"
    "/orderby/norad_cat_id asc"
    "/format/json"
)

OUT_PATH = Path("spacetrack_snapshot.json")


def main():
    with requests.Session() as session:
        login_resp = session.post(
            LOGIN_URL,
            data={"identity": SPACE_TRACK_USER, "password": SPACE_TRACK_PASS},
            timeout=30,
        )
        login_resp.raise_for_status()

        resp = session.get(QUERY_URL, timeout=120)
        resp.raise_for_status()

        data = resp.json()
        OUT_PATH.write_text(json.dumps(data), encoding="utf-8")
        print(f"Saved {len(data)} records to {OUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
