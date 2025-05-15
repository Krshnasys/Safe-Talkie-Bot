# Safe Talkie Bot

Safe Talkie Bot is a simple Telegram bot that removes abusive messages and links from groups to keep them clean and safe. With admin-only commands and robust filtering, it ensures a respectful chat environment.

## 🚀 Deployment Guide

Follow these steps to deploy Safe Talkie Bot on Heroku.

### Prerequisites

- Python 3.13+ ([Download](https://www.python.org/downloads/))
- Telegram Bot Token from [BotFather](https://t.me/BotFather)
- Heroku Account ([Sign Up](https://signup.heroku.com/))
- Git installed

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Krshnasys/Safe-Talkie-Bot.git
   cd Safe-Talkie-Bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Bot**:
   - Copy `config.json.example` to `config.json`:
     ```json
     {
       "telegram_api_id": "your_api_id",
       "telegram_api_hash": "your_api_hash",
       "telegram_bot_token": "your_bot_token",
       "admins": [7533858093],
       "auth_groups": [-1002573318527],
       "use_auth": true,
       "delete_urls": true,
       "memory_threshold": 512
     }
     ```
   - Get `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).
   - Add bad words to `bad_words.txt` (one per line, e.g., `exchange`).

4. **Set Up Heroku**:
   ```bash
   heroku login
   heroku create safe-talkie-bot
   heroku config:set CONFIG_FILE=config.json
   heroku config:set LOG_LEVEL=DEBUG
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   heroku ps:scale worker=1
   ```

6. **Verify**:
   - Check logs: `heroku logs --tail`
   - Test `/start` as an admin in PM or `/id` in an authorized group.

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
