import requests
import os
import feedparser

RSS_URL = "https://www.reddit.com/r/projectmanagement/.rss"

feed = feedparser.parse(RSS_URL)

posts = []

for entry in feed.entries[:5]:

    title = entry.title
    link = entry.link

    summary = ""

    if hasattr(entry, "summary"):
        summary = entry.summary

        # تنظيف HTML بسيط
        summary = (
            summary.replace("<p>", "")
            .replace("</p>", "")
            .replace("<br />", " ")
            .replace("&amp;", "&")
        )

        summary = summary[:300]

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
