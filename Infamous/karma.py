# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX
# https://t.me/O_okarma

# <============================================== IMPORTS =========================================================>
from pyrogram.types import InlineKeyboardButton as ib
from telegram import InlineKeyboardButton

from Mikobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT

# <============================================== CONSTANTS =========================================================>
START_IMG = [
    "https://telegra.ph/file/63d3159644e518947e654.jpg",
    "https://telegra.ph/file/c7749599d0e4bf2071569.jpg",
    "https://telegra.ph/file/1e06b91bd52ec768de2bb.jpg",
    "https://telegra.ph/file/460f91ba860f2e6bf9144.jpg",
    "https://telegra.ph/file/9c28cddd0df594fcd6b8a.jpg",
    "https://telegra.ph/file/52475013ea9e235eb725e.jpg",
    "https://telegra.ph/file/43f7d43e5ad5a5601f093.jpg",
]

HEY_IMG = "https://telegra.ph/file/c3616f6a49f181e9a210f.jpg"

ALIVE_ANIMATION = [
    "https://telegra.ph/file/bf67a97683bfa26244053.mp4",
    "https://telegra.ph/file/ff7bd96efc1bab7f7ed1a.mp4",
    "https://telegra.ph/file/e5fa0dc80f16adbb87fe6.mp4",
    "https://telegra.ph/file/b0e9860b6fd6f636ee89b.mp4",
    "https://telegra.ph/file/a6c1c4bb185430756ab48.mp4",
    "https://telegra.ph/file/26f3749531e0712aba2fb.mp4",
    "https://telegra.ph/file/0d81f282f19b652415bac.mp4",
    "https://telegra.ph/file/3f98d29f7e50e589d60d1.mp4",
]

FIRST_PART_TEXT = "🪷 *ʜᴇʏ* `{}` . . ."

PM_START_TEXT = "🫧 *ɪ ᴀᴍ ᴍs ʟɪcʜᴀ 🫧, ᴀ ᴛʜᴇᴍᴇᴅ ʙᴏᴛ ᴡʜɪᴄʜ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴀɴᴅ sᴇᴄᴜʀᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ʜᴜɢᴇ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴍᴇɴɴᴛ ᴇᴄᴏsʏsᴛᴇᴍ*"

START_BTN = [
    [
        InlineKeyboardButton(
            text="⛩️ sᴜᴍᴍᴏɴ ᴍᴇ ⛩️",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="🌀 ʜᴇʟᴘ 🌀", callback_data="help_back"),
    ],
    [
        InlineKeyboardButton(text="🏮 ᴅᴇᴛᴀɪʟs 🏮", callback_data="Miko_"),
        InlineKeyboardButton(text="🌪 ᴀɪ 🌪", callback_data="ai_handler"),
    ],
]

GROUP_START_BTN = [
    [
        InlineKeyboardButton(
            text="⛩️ sᴜᴍᴍᴏɴ ᴍᴇ ⛩️",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="🌪 sᴜᴩᴩᴏʀᴛ 🌪", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
]

ALIVE_BTN = [
    [
        ib(text="UPDATES", url="https://t.me/Hydra_Updates"),
        ib(text="SUPPORT", url="https://t.me/hydraXsupport"),
    ],
    [
        ib(
            text="⇦ ADD ME ⇨",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = """
🫧 *Yae-Miko* 🫧

☉ *Here, you will find a list of all the available commands.*

ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /
"""
