import feedparser
import requests
import os

RSS_URL = "https://www.reddit.com/r/projectmanagement/.rss"

feed = feedparser.parse(RSS_URL)

posts = []

for entry in feed.entries[:5]:
    posts.append(
        f"📌 {entry.title}\n{entry.link}"
    )

message = "📊 Project Management Daily Report\n\n"
message += "\n\n".join(posts)

requests.post(
    f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
    data={
        "chat_id": os.environ["TELEGRAM_CHAT_ID"],
        "text": message
    }
)
