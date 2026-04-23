import requests
import os

URL = "https://data.ninjakiwi.com/btd6/ct"

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
LAST_ID = os.environ.get("LAST_ID", "")

data = requests.get(URL, timeout=15).json()
event = data["body"][0]

latest = event["id"]

if latest != LAST_ID:

    # Convert milliseconds to Unix seconds for Discord timestamps
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

    requests.post(WEBHOOK, json=payload)

    with open("last_id.txt", "w") as f:
        f.write(latest)
