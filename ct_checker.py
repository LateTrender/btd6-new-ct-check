import requests
import os
import time

URL = "https://data.ninjakiwi.com/btd6/ct"

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
LAST_ID = os.environ.get("LAST_ID", "")

def fetch_json():
    for attempt in range(3):
        try:
            r = requests.get(URL, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)

    raise Exception("API failed after 3 attempts")

data = fetch_json()

event = data["body"][0]
latest = event["id"]

if latest != LAST_ID:

    start_unix = event["start"] // 1000
    end_unix = event["end"] // 1000

    payload = {
        "embeds": [
            {
                "title": "🔥 New Contested Territory Event Detected!",
                "color": 16753920,
                "fields": [
                    {
                        "name": "CT ID",
                        "value": latest,
                        "inline": True
                    },
                    {
                        "name": "Starts",
                        "value": f"<t:{start_unix}:F>",
                        "inline": False
                    },
                    {
                        "name": "Ends",
                        "value": f"<t:{end_unix}:F>",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Bloons TD 6 CT Tracker"
                }
            }
        ]
    }

    requests.post(WEBHOOK, json=payload, timeout=15)

    with open("last_id.txt", "w") as f:
        f.write(latest)

else:
    print("No new CT event.")
