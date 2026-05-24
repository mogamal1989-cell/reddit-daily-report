import os
import requests
import feedparser
from bs4 import BeautifulSoup

RSS_URL = "https://www.reddit.com/r/projectmanagement/.rss"

feed = feedparser.parse(RSS_URL)

posts = []

for entry in feed.entries[:5]:

    title = entry.title
    link = entry.link

    summary = ""

    if hasattr(entry, "summary"):

        soup = BeautifulSoup(
            entry.summary,
            "html.parser"
        )

        summary = soup.get_text(
            separator=" ",
            strip=True
        )

        summary = summary.replace("SC_OFF", "")
        summary = summary.replace("SC_ON", "")

        if len(summary) > 400:
            summary = summary[:400] + "..."

    post = f"""
📌 {title}

📝 {summary}

🔗 {link}
"""

    posts.append(post)

message = "📊 Project Management Daily Report\n"

for post in posts:

    candidate = (
        message
        + "\n━━━━━━━━━━━━━━\n"
        + post
    )

    if len(candidate) < 3800:
        message = candidate

response = requests.post(
    f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
    data={
        "chat_id": os.environ["TELEGRAM_CHAT_ID"],
        "text": message
    },
    timeout=30
)

print("Telegram Status:", response.status_code)
print(response.text)
