# <============================================== IMPORTS =========================================================>
import html
import time
from datetime import datetime
from io import BytesIO

from telegram import ChatMemberAdministrator, Update
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden, TelegramError
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from telegram.helpers import mention_html

import Database.sql.global_bans_sql as sql
from Database.sql.users_sql import get_user_com_chats
from Mikobot import (
    DEV_USERS,
    DRAGONS,
    EVENT_LOGS,
    OWNER_ID,
    STRICT_GBAN,
    SUPPORT_CHAT,
    dispatcher,
    function,
)
from Mikobot.plugins.helper_funcs.chat_status import (
    check_admin,
    is_user_admin,
    support_plus,
)
from Mikobot.plugins.helper_funcs.extraction import extract_user, extract_user_and_text
from Mikobot.plugins.helper_funcs.misc import send_to_list

# <=======================================================================================================>

GBAN_ENFORCE_GROUP = 6

GBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Peer_id_invalid",
    "Group chat was deactivated",
    "Need to be inviter of a user to kick it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can kick group administrators",
    "Channel_private",
    "Not in the chat",
    "Can't remove chat owner",
}

UNGBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Method is available for supergroup and channel chats only",
    "Not in the chat",
    "Channel_private",
    "Chat_admin_required",
    "Peer_id_invalid",
    "User not found",
}


# <================================================ FUNCTION =======================================================>
async def gban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id, reason = await extract_user_and_text(message, context, args)

    if not user_id:
        await message.reply_text(
            "You don't seem to be referring to a user or the ID specified is incorrect..",
        )
        return

    if int(user_id) in DEV_USERS:
        await message.reply_text(
            "That user is part of the Association\nI can't act against our own.",
        )
        return

    if int(user_id) in DRAGONS:
        await message.reply_text(
            "I spy, with my little eye... a disaster! Why are you guys turning on each other?",
        )
        return

    if user_id == bot.id:
        await message.reply_text("You uhh...want me to kick myself?")
        return

    if user_id in [777000, 1087968824]:
        await message.reply_text("Fool! You can't attack Telegram's native tech!")
        return

    try:
        user_chat = await bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            await message.reply_text("I can't seem to find this user.")
            return ""
        else:
            return

    if user_chat.type != "private":
        await message.reply_text("That's not a user!")
        return

    if sql.is_user_gbanned(user_id):
        if not reason:
            await message.reply_text(
                "This user is already gbanned; I'd change the reason, but you haven't given me one...",
            )
            return

        old_reason = sql.update_gban_reason(
            user_id,
            user_chat.username or user_chat.first_name,
            reason,
        )
        if old_reason:
            await message.reply_text(
                "This user is already gbanned, for the following reason:\n"
                "<code>{}</code>\n"
                "I've gone and updated it with your new reason!".format(
                    html.escape(old_reason),
                ),
                parse_mode=ParseMode.HTML,
            )

        else:
            await message.reply_text(
                "This user is already gbanned, but had no reason set; I've gone and updated it!",
            )

        return

    # Sending approval request to the support group
    approval_message = (
        f"Admin {mention_html(user.id, user.first_name)} requests to gban user "
        f"{mention_html(user_chat.id, user_chat.first_name)} ({user_chat.id}).\n"
        f"Reason: {html.escape(reason) if reason else 'No reason provided'}"
    )
    approval_message = await bot.send_message(
        SUPPORT_CHAT, approval_message, parse_mode=ParseMode.HTML
    )

    # Adding approval buttons
    buttons = [
        [
            InlineKeyboardButton("Approve", callback_data=f"approve_gban_{user_id}"),
            InlineKeyboardButton("Reject", callback_data=f"reject_gban_{user_id}"),
        ]
    ]
    approval_message.edit_reply_markup(InlineKeyboardMarkup(buttons))


async def gban_approval_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    data = query.data

    if data.startswith("approve_gban_"):
        user_id = int(data.split("_")[2])
        await context.bot.answer_callback_query(query.id, "Gban approved")
        await context.bot.delete_message(query.message.chat_id, query.message.message_id)
        await apply_gban(context, user_id, user)

    elif data.startswith("reject_gban_"):
        await context.bot.answer_callback_query(query.id, "Gban rejected")
        await context.bot.delete_message(query.message.chat_id, query.message.message_id)


async def apply_gban(context, user_id, admin_user):
    bot = context.bot
    user_chat = await bot.get_chat(user_id)
    start_time = time.time()
    datetime_fmt = "%Y-%m-%dT%H:%M"
    current_time = datetime.utcnow().strftime(datetime_fmt)

    log_message = (
        f"#GBANNED\n"
        f"<b>Originated from:</b> Global Ban Request\n"
        f"<b>Admin:</b> {mention_html(admin_user.id, admin_user.first_name)}\n"
        f"<b>Banned User:</b> {mention_html(user_chat.id, user_chat.first_name)}\n"
        f"<b>Banned User ID:</b> <code>{user_chat.id}</code>\n"
        f"<b>Event Stamp:</b> <code>{current_time}</code>"
    )

    if EVENT_LOGS:
        try:
            log = await bot.send_message(
                EVENT_LOGS, log_message, parse_mode=ParseMode.HTML
            )
        except BadRequest as excp:
            log = await bot.send_message(
                EVENT_LOGS,
                log_message
                + "\n\nFormatting has been disabled due to an unexpected error.",
            )
    else:
        send_to_list(bot, DRAGONS, log_message, html=True)

    sql.gban_user(user_id, user_chat.username or user_chat.first_name, reason)

    chats = get_user_com_chats(user_id)
    gbanned_chats = 0

    for chat in chats:
        chat_id = int(chat)

        # Check if this group has disabled gbans
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            await bot.ban_chat_member(chat_id, user_id)
            gbanned_chats += 1

        except BadRequest as excp:
            if excp.message in GBAN_ERRORS:
                pass
            else:
                if EVENT_LOGS:
                    await bot.send_message(
                        EVENT_LOGS,
                        f"Could not gban due to {excp.message}",
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    send_to_list(
                        bot,
                        DRAGONS,
                        f"Could not gban due to: {excp.message}",
                    )
                sql.ungban_user(user_id)
                return
        except TelegramError:
            pass

    if EVENT_LOGS:
        await log.edit_text(
            log_message + f"\n<b>Chats affected:</b> <code>{gbanned_chats}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        send_to_list(
            bot,
            DRAGONS,
            f"Gban complete! (User banned in <code>{gbanned_chats}</code> chats)",
            html=True,
        )

    end_time = time.time()
    gban_time = round((end_time - start_time), 2)

    if gban_time > 60:
        gban_time = round((gban_time / 60), 2)

    try:
        await bot.send_message(
            user_id,
            "#EVENT"
            "You have been marked as Malicious and as such have been banned from any future groups we manage."
            f"\n<b>Reason:</b> <code>{html.escape(user.reason)}</code>"
            f"</b>Appeal Chat:</b> @{SUPPORT_CHAT}",
            parse_mode=ParseMode.HTML,
        )
    except:
        pass  # bot probably blocked by user


async def ungban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective