import requests
import os
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
        " ",
        strip=True
    )

    summary = summary[:350]

    posts.append(
        f"📌 {title}\n\n"
        f"📝 {summary}\n\n"
        f"🔗 {link}"
    )

message = "📊 Project Management Daily Report\n\n"

for post in posts:
    temp = message + "\n\n━━━━━━━━━━━━━━\n\n" + post

    if len(temp) < 3800:
        message = temp

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
