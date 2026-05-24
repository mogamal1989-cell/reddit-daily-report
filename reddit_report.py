import requests
import os
from datetime import datetime, timezone, timedelta

URL = "https://www.reddit.com/r/projectmanagement/top.json?t=day&limit=10"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
data = response.json()

posts = []

for post in data["data"]["children"]:

    p = post["data"]

    title = p["title"]
    score = p["score"]
    comments = p["num_comments"]
    text = p.get("selftext", "")

    summary = text[:250].replace("\n", " ")

    if len(summary) > 250:
        summary += "..."

    link = "https://reddit.com" + p["permalink"]

    posts.append(
        f"📌 {title}\n\n"
        f"👍 {score} | 💬 {comments}\n\n"
        f"📝 {summary}\n\n"
        f"🔗 {link}"
    )

message = "📊 Project Management Daily Report\n\n"
message += "\n\n━━━━━━━━━━━━━━\n\n".join(posts[:5])

requests.post(
    f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
    data={
        "chat_id": os.environ["TELEGRAM_CHAT_ID"],
        "text": message[:4000]
    }
)
