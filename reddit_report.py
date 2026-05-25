import os
import feedparser
import requests
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

    summary = ""

    if hasattr(entry, "summary"):
        summary = entry.summary

    summary = summary.replace("<p>", "").replace("</p>", "")
    summary = summary.replace("&amp;", "&")
    summary = summary.replace("\n", " ")

    if len(summary) > 400:
        summary = summary[:400] + "..."

    message += f"""
📌 {title}

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
