import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from Helpers.config import load_config
from Helpers.utils import is_abusive, monitor_memory, handle_message
from Helpers.metrics import MetricsCollector
from bot.basic_cmds import start, user_info, show_id_pm, show_id_group

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

config = load_config()
bad_words = config.load_bad_words()
metrics = MetricsCollector()
app = Client(
    "my_bot",
    api_id=config.telegram_api_id,
    api_hash=config.telegram_api_hash,
    bot_token=config.telegram_bot_token,
    workers=1
)

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    await start(client, message, config, metrics)

app.on_message(filters.command(["info"], prefixes=["/", "!"]) & (filters.group | filters.private))(user_info)
app.on_message(filters.command(["id"], prefixes=["/", "!"]) & filters.private)(show_id_pm)
app.on_message(filters.command(["id"], prefixes=["/", "!"]) & filters.group)(show_id_group)

@app.on_message(filters.text & filters.group)
async def group_message_handler(client: Client, message: Message):
    try:
        metrics.increment_message_count()
        await handle_message(client, message, bad_words, config, metrics)
    except Exception as e:
        logger.error(f"Error handling group message: {e}", exc_info=True)
        metrics.increment_error_count()

if __name__ == "__main__":
    try:
        app.loop.create_task(monitor_memory(config, metrics))
        logger.info("Bot starting...")
        metrics.record_bot_start()
        app.run()
    except Exception as e:
        logger.error(f"Bot failed to start: {e}", exc_info=True)
        metrics.increment_error_count()
        raise
