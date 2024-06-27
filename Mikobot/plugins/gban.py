from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler

# Assuming you have a way to identify sudoers, modify as per your existing logic
def is_sudoer(user_id):
    return user_id in DEV_USERS  # Update with your sudoers' IDs

@support_plus
async def gban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot, args = context.bot, context.args
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id, reason = await extract_user_and_text(message, context, args)

    if not user_id:
        await message.reply_text("You need to specify a user to globally ban.")
        return

    if is_sudoer(user.id):  # Check if the user initiating the gban is a sudoer
        await message.reply_text("Your global ban request is under review.")
        
        # Send ban request to support group for approval
        approval_message = (
            f"🚫 Global Ban Request 🚫\n\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User to Ban:</b> <code>{user_id}</code>\n"
            f"<b>Reason:</b> <code>{reason}</code>\n\n"
            f"Please review and approve this request."
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Approve", callback_data=f"approve_gban_{user_id}_{reason}")],
            [InlineKeyboardButton("Reject", callback_data=f"reject_gban_{user_id}")]
        ])

        approval_message = await bot.send_message(SUPPORT_CHAT, approval_message, parse_mode=ParseMode.HTML, reply_markup=keyboard)

        # Wait for approval via callback query
        context.dispatcher.add_handler(CallbackQueryHandler(handle_gban_approval))

    else:
        await message.reply_text("You are not authorized to initiate a global ban.")

async def handle_gban_approval(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = int(query.data.split("_")[2])  # Extract user_id from callback_data
    reason = "_".join(query.data.split("_")[3:])  # Extract reason from callback_data
    user = query.from_user
    chat = query.message.chat

    if query.data.startswith("approve_gban"):
        await query.answer("Global ban approved!")

        # Perform the global ban
        # Include your existing gban logic here
        # Example:
        # await perform_global_ban(user_id, user, chat, reason)
        # Replace with your actual logic to perform the global ban

    elif query.data.startswith("reject_gban"):
        await query.answer("Global ban request rejected.")
        await bot.send_message(user_id, "Your global ban request has been rejected.")

    # Cleanup
    await query.message.delete()

# Ensure this function is added to your handlers
dispatcher.add_handler(CallbackQueryHandler(handle_gban_approval))