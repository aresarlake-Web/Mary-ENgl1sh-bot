"""
Free-text message handler for private chats and group chats.
"""

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from app.services.ai_service import ask_ai
from app.services.memory_service import (
    get_group_history,
    get_private_history,
    save_group,
    save_private,
)
from app.services.quiz_service import check_quiz_answer


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle non-command text messages in private and group chats.

    Private chats: every message is sent to the AI with the user's private
    history as context.

    Group chats: first checks for an active quiz answer, then only responds
    if the bot is mentioned, replied to, or the message starts with "alex".
    """
    if not update.message or not update.message.text:
        return

    chat_type = update.effective_chat.type
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    bot_username = context.bot.username

    # ── PRIVATE CHAT ──
    if chat_type == "private":
        await update.message.chat.send_action(ChatAction.TYPING)
        reply = await ask_ai(get_private_history(user_id), text)
        save_private(user_id, "user", text)
        save_private(user_id, "assistant", reply)
        await update.message.reply_text(reply)
        return

    # ── GROUP CHAT ──
    # Check if answering a quiz first
    if await check_quiz_answer(update, context):
        return

    # Bot responds if:
    # 1. Someone tagged @botusername
    # 2. Someone replied to the bot's message
    # 3. Message starts with "Alex" or "alex"
    is_mentioned = bot_username and f"@{bot_username}" in text
    is_reply_to_bot = (
        update.message.reply_to_message
        and update.message.reply_to_message.from_user
        and update.message.reply_to_message.from_user.id == context.bot.id
    )
    is_called = text.lower().startswith("alex")

    if not (is_mentioned or is_reply_to_bot or is_called):
        return

    # Clean the message (remove @mention)
    clean_text = text.replace(f"@{bot_username}", "").strip()
    if not clean_text:
        clean_text = "Hello!"

    user_name = update.effective_user.first_name or "friend"
    prompt = f"{user_name} says: {clean_text}"

    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await ask_ai(get_group_history(chat_id), prompt)

    save_group(chat_id, "user", prompt)
    save_group(chat_id, "assistant", reply)

    await update.message.reply_text(reply)
