import os
import feedparser
import requests
import re
from datetime import datetime

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

RSS_URL = "https://www.reddit.com/r/projectmanagement/new/.rss"

headers = {
    "User-Agent": "Mozilla/5.0"
}

feed = feedparser.parse(RSS_URL)

today = datetime.now().strftime("%d/%m/%Y")

message = f"""
☀️ صباح الخير يا محمد

📚 تقرير Project Management اليومي

📅 {today}

تم مراجعة أحدث المواضيع المنشورة على Reddit واختيار أبرز النقاشات الجديدة التي قد تهمك اليوم.

━━━━━━━━━━━━━━

"""

for entry in feed.entries[:5]:

    title = entry.title
    link = entry.link

    score = "N/A"
    comments = "N/A"

    try:
        json_url = link.rstrip("/") + ".json"

        response = requests.get(
            json_url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            post_data = data[0]["data"]["children"][0]["data"]

            score = post_data.get("score", "N/A")
            comments = post_data.get("num_comments", "N/A")

    except Exception:
        pass

    summary = ""

    if hasattr(entry, "summary"):
        summary = entry.summary

    summary = re.sub(r"<.*?>", "", summary)
    summary = summary.replace("&amp;", "&")
    summary = summary.replace("\n", " ")

    if len(summary) > 400:
        summary = summary[:400] + "..."

    message += f"""
📌 {title}

👍 Score: {score}
💬 Comments: {comments}

📝 {summary}

🔗 {link}

━━━━━━━━━━━━━━

"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Report sent successfully")
