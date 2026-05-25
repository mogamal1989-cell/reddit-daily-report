import os
import requests
from datetime import datetime

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.reddit.com/r/projectmanagement/new.json?limit=10"

response = requests.get(url, headers=headers)
data = response.json()

today = datetime.now().strftime("%d/%m/%Y")

message = f"""
☀️ صباح الخير يا محمد

📚 تقرير Project Management اليومي

📅 {today}

تم مراجعة أحدث المواضيع المنشورة على Reddit واختيار أبرز النقاشات الجديدة التي قد تهمك اليوم.

━━━━━━━━━━━━━━

"""

for post in data["data"]["children"][:5]:

    post_data = post["data"]

    title = post_data["title"]
    score = post_data["score"]
    comments = post_data["num_comments"]
    content = post_data.get("selftext", "")
    link = "https://www.reddit.com" + post_data["permalink"]

    if len(content) > 400:
        content = content[:400] + "..."

    if content.strip() == "":
        content = "No text content available."

    message += f"""
📌 {title}

👍 Score: {score}
💬 Comments: {comments}

📝 {content}

🔗 {link}

━━━━━━━━━━━━━━

"""

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print("Report sent successfully")
