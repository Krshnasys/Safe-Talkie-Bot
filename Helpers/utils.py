import re
import logging
import asyncio
import psutil
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError
from Scripts import Scripts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MessageLock:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.processed_ids = set()

    async def process(self, message_id):
        async with self.lock:
            if message_id in self.processed_ids:
                logger.debug(f"Message {message_id} already processed, skipping")
                return False
            self.processed_ids.add(message_id)
            logger.debug(f"Acquired lock for message {message_id}")
            return True

    async def clear(self):
        async with self.lock:
            self.processed_ids.clear()
            logger.debug("Cleared processed message IDs")

message_lock = MessageLock()

async def clear_processed_ids():
    while True:
        await message_lock.clear()
        await asyncio.sleep(1)

def is_abusive(text, bad_words):
    try:
        text_lower = text.lower().strip()
        if not text_lower:
            logger.debug("Empty message text, skipping abuse check")
            return False
        matched_words = [word for word in bad_words if word in text_lower]
        if matched_words:
            logger.info(f"Abusive words detected: {matched_words}")
            return True
        logger.debug("No abusive words detected")
        return False
    except Exception as e:
        logger.error(f"Abuse check failed: {e}", exc_info=True)
        return False

async def monitor_memory(config, metrics):
    process = psutil.Process()
    total_memory = psutil.virtual_memory().total / (1024 * 1024)
    memory_threshold = min(config.memory_threshold, total_memory * 0.8)
    while True:
        try:
            mem_usage = process.memory_info().rss / (1024 * 1024)
            logger.info(f"Memory usage: {mem_usage:.2f} MB")
            metrics.record_memory_usage(mem_usage)
            if mem_usage > memory_threshold:
                logger.warning("Memory threshold exceeded, shutting down")
                await Client("my_bot").stop()
                raise SystemExit
        except psutil.Error as e:
            logger.error(f"Memory check failed: {e}", exc_info=True)
            metrics.increment_error_count()
        except Exception as e:
            logger.error(f"Memory monitor error: {e}", exc_info=True)
            metrics.increment_error_count()
        await asyncio.sleep(60)

async def handle_message(client, message, bad_words, config, metrics):
    try:
        logger.debug(f"Processing message {message.id} from chat {message.chat.id}")
        if not await message_lock.process(message.id):
            return

        if config.use_auth and message.chat.id not in config.auth_groups:
            logger.debug(f"Unauthorized chat {message.chat.id}, skipping")
            return

        text = message.text or message.caption or ""
        if not text:
            logger.debug(f"No text or caption in message {message.id}, skipping")
            return

        bot = await client.get_me()
        if message.from_user and (message.from_user.id == bot.id or message.from_user.id in config.admins):
            logger.debug(f"Skipping message {message.id} from bot or admin {message.from_user.id}")
            return

        mention = message.from_user.mention if message.from_user else "User"
        url_pattern = r"(https?://|www\.|t\.me/|telegram\.me/)[^\s]+"
        if config.delete_urls and re.search(url_pattern, text, re.IGNORECASE):
            try:
                logger.info(f"Deleting message {message.id} with URL from user {message.from_user.id}")
                await message.delete()
                await client.send_message(message.chat.id, Scripts.LINK_DELETE_TXT.format(mention=mention), reply_to_message_id=None)
                metrics.increment_url_deletions()
                return
            except FloodWait as e:
                logger.info(f"FloodWait: Sleeping for {e.value} seconds")
                await asyncio.sleep(e.value)
            except RPCError as e:
                logger.warning(f"Failed to handle URL message {message.id}: {e}")
                metrics.increment_error_count()
            return

        if is_abusive(text, bad_words):
            try:
                logger.info(f"Deleting abusive message {message.id} from user {message.from_user.id}")
                await message.delete()
                await client.send_message(message.chat.id, Scripts.WARN_TXT.format(mention=mention), reply_to_message_id=None)
                metrics.increment_abuse_deletions()
            except FloodWait as e:
                logger.info(f"FloodWait: Sleeping for {e.value} seconds")
                await asyncio.sleep(e.value)
            except RPCError as e:
                logger.warning(f"Failed to handle abusive message {message.id}: {e}")
                metrics.increment_error_count()
    except Exception as e:
        logger.error(f"Message handling failed for message {message.id}: {e}", exc_info=True)
        metrics.increment_error_count()
