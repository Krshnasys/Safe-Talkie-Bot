# Safe Talkie Bot

Safe Talkie Bot is a simple Telegram bot that removes abusive messages and links from groups to keep them clean and safe.

## Deployment Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Krshnasys/Safe-Talkie-Bot.git
cd Safe-Talkie-Bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Configuration

Copy the example config file and edit with your details:

```bash
cp config.json.example config.json
```

Update `config.json` like this:

```json
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
```

### 4. Deploy to Heroku

```bash
heroku login
heroku create safe-talkie-bot
heroku config:set CONFIG_FILE=config.json
heroku config:set LOG_LEVEL=DEBUG
```

### 5. Push and Run the Bot

```bash
git push heroku main
heroku ps:scale worker=1
```
