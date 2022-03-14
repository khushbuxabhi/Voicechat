import asyncio
from time import time
from datetime import datetime
from driver.filters import command
from config import BOT_NAME as bn, BOT_USERNAME, SUPPORT_GROUP, OWNER_USERNAME
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from program import __version__, LOGS
from pytgcalls import (__version__ as pytover)

from driver.filters import command
from driver.core import bot, me_bot, me_user
from driver.database.dbusers import add_served_user
from driver.database.dbchat import add_served_chat, is_served_chat
from driver.database.dblockchat import blacklisted_chats
from driver.database.dbpunish import is_gbanned_user
from driver.decorators import check_blacklist

from pyrogram import Client, filters, __version__ as pyrover
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(command("start") & filters.private & ~filters.group & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgUAAx0CZIiVngACSppiDZZGd6IPFA0TnEuOM3EqFbRxVQACCQMAArU72FSskU3O5FiqcyME")
    await message.reply_photo(
        photo=f"https://telegra.ph/file/053f99956ccee8416b8f7.jpg",
        caption=f"""**━━━━━━━━━━━━━━━━━━
🖤 ʜᴇʏ {message.from_user.mention()} !

         ɪ ᴀᴍ [{bn}](t.me/{BOT_USERNAME}) sᴜᴘᴇʀ ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs...
ᴀʟʟ ᴏꜰ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /
┏━━━━━━━━━━━━━━┓
┣★
┣★ ᴄʀᴇᴀᴛᴏʀ: [𝝙𝗡𝗢𝗡𝗬𝗠𝗢𝗨𝗦](t.me/{OWNER_USERNAME})
┣★
┗━━━━━━━━━━━━━━┛

💞 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ ᴅᴍ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](t.me/{OWNER_USERNAME}) ʙᴀʙʏ...
━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✗ ᴀᴅᴅ ᴍᴇ ᴇʟsᴇ ʏᴏᴜ ɢᴇʏ​ ✗", url="https://t.me/{}?startgroup=true".format(BOT_USERNAME)
                       ),
                  ],[
                    InlineKeyboardButton(
                        "✗ ᴅᴇᴠᴇʟᴏᴘᴇʀ ✗", url="https://t.me/{}".format(OWNER_USERNAME)
                    ),
                    InlineKeyboardButton(
                        "✗ sᴜᴘᴘᴏʀᴛ ✗", url="https://t.me/{}".format(SUPPORT_GROUP)
                    )
                ],[ 
                    InlineKeyboardButton(
                        "✗ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ​ ✗", url="https://t.me/DevilsHeavenMF"
                    )]
            ]
       ),
    )

@Client.on_message(command(["ping", "repo", "anon", "alive"]) & filters.group & ~filters.edited & ~filters.private)

async def help(client: Client, message: Message):
    await message.reply_sticker("CAACAgUAAx0CZIiVngACSppiDZZGd6IPFA0TnEuOM3EqFbRxVQACCQMAArU72FSskU3O5FiqcyME")
    await message.reply_text(
        text=f"""» ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✗ ᴅᴇᴠᴇʟᴏᴘᴇʀ ✗", url="https://t.me/{}".format(OWNER_USERNAME) )
                  ],[
                    InlineKeyboardButton(
                        "✗ sᴜᴘᴘᴏʀᴛ ✗", url="https://t.me/{}".format(SUPPORT_GROUP)
                    ),
                    InlineKeyboardButton(
                        "✗ sᴏᴜʀᴄᴇ ✗", url="https://t.me/DevilsHeavenMF"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "✗ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ​​ ✗", url="https://t.me/{}?startgroup=true".format(BOT_USERNAME)
                    )]
            ]
        ),
    )
