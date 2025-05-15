Safe Talkie Bot

Safe Talkie Bot is a lightweight Telegram group moderation bot that automatically deletes abusive messages and unwanted links to help keep your group clean and safe.


---

Deployment Guide

1. Clone the Repository

git clone https://github.com/Krshnasys/Safe-Talkie-Bot.git
cd Safe-Talkie-Bot

2. Install Dependencies

pip install -r requirements.txt

3. Configure the Bot

Copy the example config file and update it with your values:

cp config.json.example config.json

Edit config.json:

{
  "telegram_api_id": "YOUR_API_ID",
  "telegram_api_hash": "YOUR_API_HASH",
  "telegram_bot_token": "YOUR_BOT_TOKEN",
  "DELETE_URLS": true,
  "ADMINS": [123456789, 987654321],
  "USE_AUTH": true,
  "AUTH_GROUPS": [-1001234567890],
  "MEMORY_THRESHOLD": 450,
  "MESSAGE_RATE_LIMIT": 100
}

4. Deploy to Heroku

heroku login
heroku create safe-talkie-bot
heroku config:set CONFIG_FILE=config.json
heroku config:set LOG_LEVEL=DEBUG

5. Push to Heroku and Start Bot

git push heroku main
heroku ps:scale worker=1


---

Let me know if you'd like a badge section, bot command list, or usage instructions added.
