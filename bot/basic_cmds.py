from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType
import logging
from Scripts import Scripts
from Helpers.utils import message_lock

logger = logging.getLogger(__name__)

async def start(client: Client, message: Message, config, metrics):
    try:
        logger.info(f"Processing /start for user {message.from_user.id}")
        if not await message_lock.process(message.id):
            return
        if message.from_user.id in config.admins:
            logger.info(f"Admin {message.from_user.id} exempted from auth check")
            bot_username = (await client.get_me()).username
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Add me to your Group", url=f"http://t.me/{bot_username}?startgroup=true")]
            ])
            await client.send_message(message.chat.id, Scripts.START_TXT, reply_to_message_id=None, reply_markup=buttons)
            metrics.increment_message_count()
            logger.info(f"Sent /start response for admin {message.from_user.id}")
            return
        if message.chat.type == ChatType.PRIVATE or (config.use_auth and message.chat.id not in config.auth_groups):
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Source Code", url="https://github.com/Krshnasys/Safe-Talkie-Bot")]
            ])
            await client.send_message(message.chat.id, Scripts.UNAUTHORIZED_GROUP_TXT, reply_to_message_id=None, reply_markup=buttons)
            metrics.increment_error_count()
            logger.info(f"Sent unauthorized response for non-admin {message.from_user.id} in chat {message.chat.id}")
            return
        bot_username = (await client.get_me()).username
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add me to your Group", url=f"http://t.me/{bot_username}?startgroup=true")]
        ])
        await client.send_message(message.chat.id, Scripts.START_TXT, reply_to_message_id=None, reply_markup=buttons)
        metrics.increment_message_count()
        logger.info(f"Sent /start response for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Failed to process /start: {e}", exc_info=True)
        await client.send_message(message.chat.id, "Error: Unable to process command", reply_to_message_id=None)

async def user_info(client: Client, message: Message):
    try:
        logger.info(f"Processing /info for user {message.from_user.id}")
        if not await message_lock.process(message.id):
            return
        target = message.reply_to_message.from_user if message.reply_to_message else message.from_user
        if not target:
            logger.error("No target user found for /info")
            await client.send_message(message.chat.id, "Error: No user found", reply_to_message_id=None)
            return
        dc_id = getattr(target, "dc_id", "Unknown")
        text = Scripts.USER_INFO_TXT.format(
            id=target.id,
            first_name=target.first_name or "None",
            username=f"@{target.username}" if target.username else "None",
            link=f"<a href='tg://user?id={target.id}'>Click here</a>",
            dc=dc_id,
            premium="Yes" if hasattr(target, "is_premium") and target.is_premium else "No"
        )
        await client.send_message(message.chat.id, text, reply_to_message_id=None)
        logger.info(f"Sent user info for user {target.id}")
    except Exception as e:
        logger.error(f"Failed to process /info: {e}", exc_info=True)
        await client.send_message(message.chat.id, "Error: Unable to fetch user info", reply_to_message_id=None)

async def show_id_pm(client: Client, message: Message):
    try:
        logger.info(f"Processing /id in PM for user {message.from_user.id}")
        if not await message_lock.process(message.id):
            return
        if message.reply_to_message:
            target = message.reply_to_message.from_user if message.reply_to_message.from_user else message.from_user
            mention = getattr(target, "mention", "User") if target else "User"
            if hasattr(message.reply_to_message, "forward_from_chat") and message.reply_to_message.forward_from_chat and message.reply_to_message.forward_from_chat.type == ChatType.CHANNEL:
                channel = message.reply_to_message.forward_from_chat
                channel_title = getattr(channel, "title", "Unknown")
                channel_id = getattr(channel, "id", "Unknown")
                logger.info(f"Channel detected in PM: title={channel_title}, id={channel_id}")
                text = Scripts.FORWARDED_CHANNEL_ID_TXT.format(
                    mention=mention,
                    user_id=target.id,
                    channel_title=channel_title,
                    channel_id=channel_id
                )
                await client.send_message(message.chat.id, text, reply_to_message_id=None)
            else:
                logger.info(f"No channel forward detected in PM, replying with user ID: {target.id}")
                await client.send_message(message.chat.id, Scripts.SELF_ID_TXT.format(id=target.id), reply_to_message_id=None)
        else:
            logger.info(f"No reply message in PM, replying with user ID: {message.from_user.id}")
            await client.send_message(message.chat.id, Scripts.SELF_ID_TXT.format(id=message.from_user.id), reply_to_message_id=None)
        logger.info(f"Sent /id response in PM for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Failed to process /id in PM: {e}", exc_info=True)
        await client.send_message(message.chat.id, "Error: Unable to fetch ID", reply_to_message_id=None)

async def show_id_group(client: Client, message: Message):
    try:
        logger.info(f"Processing /id in group for chat {message.chat.id}")
        if not await message_lock.process(message.id):
            return
        if message.reply_to_message:
            target = message.reply_to_message.from_user if message.reply_to_message.from_user else message.from_user
            mention = getattr(target, "mention", "User") if target else "User"
            if hasattr(message.reply_to_message, "forward_from_chat") and message.reply_to_message.forward_from_chat and message.reply_to_message.forward_from_chat.type == ChatType.CHANNEL:
                channel = message.reply_to_message.forward_from_chat
                channel_title = getattr(channel, "title", "Unknown")
                channel_id = getattr(channel, "id", "Unknown")
                logger.info(f"Channel detected: title={channel_title}, id={channel_id}")
                text = Scripts.FORWARDED_CHANNEL_ID_TXT.format(
                    mention=mention,
                    user_id=target.id,
                    channel_title=channel_title,
                    channel_id=channel_id
                )
                await client.send_message(message.chat.id, text, reply_to_message_id=None)
            else:
                logger.info(f"No channel forward detected, replying with user ID: {target.id}")
                await client.send_message(message.chat.id, Scripts.USER_ID_TXT.format(mention=mention, id=target.id), reply_to_message_id=None)
        else:
            logger.info(f"No reply message, replying with chat ID: {message.chat.id}")
            await client.send_message(message.chat.id, Scripts.CHAT_ID_TXT.format(id=message.chat.id), reply_to_message_id=None)
        logger.info(f"Sent /id response in group for chat {message.chat.id}")
    except Exception as e:
        logger.error(f"Failed to process /id in group: {e}", exc_info=True)
        await client.send_message(message.chat.id, "Error: Unable to fetch ID", reply_to_message_id=None)
