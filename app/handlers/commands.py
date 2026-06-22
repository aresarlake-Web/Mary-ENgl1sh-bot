"""
Slash-command handlers: /start, /help, /quiz, /lesson, /word, /check,
/tip, /reset.
"""

import random

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from app.data.texts import (
    CHECK_USAGE_MESSAGE,
    GRAMMAR_TIP_PROMPT,
    HELP_MESSAGE,
    LESSON_TOPICS,
    START_MESSAGE_GROUP,
    START_MESSAGE_PRIVATE,
    WORD_OF_THE_DAY_PROMPT,
)
from app.services.ai_service import ask_ai
from app.services.memory_service import (
    clear_group,
    clear_private,
    get_group_history,
    save_group,
)
from app.services.quiz_service import start_quiz


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greet the user with an intro message tailored to chat type."""
    chat_type = update.effective_chat.type
    user_name = update.effective_user.first_name or "there"

    if chat_type == "private":
        await update.message.reply_text(
            START_MESSAGE_PRIVATE.format(user_name=user_name),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await update.message.reply_text(
            START_MESSAGE_GROUP,
            parse_mode=ParseMode.MARKDOWN,
        )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the list of available commands."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)


async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a quiz in the group or private chat."""
    await start_quiz(update, context)


async def cmd_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deliver a mini English lesson on a random topic."""
    chat_id = update.effective_chat.id
    await update.message.chat.send_action(ChatAction.TYPING)

    topic = random.choice(LESSON_TOPICS)
    reply = await ask_ai(get_group_history(chat_id), topic)

    save_group(chat_id, "assistant", reply)
    await update.message.reply_text(f"📖 *Today's Lesson:*\n\n{reply}", parse_mode=ParseMode.MARKDOWN)


async def cmd_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Teach a random useful word."""
    await update.message.chat.send_action(ChatAction.TYPING)

    reply = await ask_ai([], WORD_OF_THE_DAY_PROMPT)
    await update.message.reply_text(f"✨ *Word of the Day:*\n\n{reply}", parse_mode=ParseMode.MARKDOWN)


async def cmd_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check English text supplied after the /check command for errors."""
    text_to_check = " ".join(context.args)

    if not text_to_check:
        await update.message.reply_text(CHECK_USAGE_MESSAGE, parse_mode=ParseMode.MARKDOWN)
        return

    await update.message.chat.send_action(ChatAction.TYPING)

    prompt = (
        f"Please check this English text for errors and correct it:\n\n\"{text_to_check}\"\n\n"
        "Show: 1) The corrected version 2) List each mistake and why it's wrong 3) A tip to remember the rule."
    )

    reply = await ask_ai([], prompt)
    await update.message.reply_text(f"🔍 *Text Check:*\n\n{reply}", parse_mode=ParseMode.MARKDOWN)


async def cmd_tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Give a random grammar tip."""
    await update.message.chat.send_action(ChatAction.TYPING)

    reply = await ask_ai([], GRAMMAR_TIP_PROMPT)
    await update.message.reply_text(f"💡 *Grammar Tip:*\n\n{reply}", parse_mode=ParseMode.MARKDOWN)


async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear conversation history for the current user or group."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if update.effective_chat.type == "private":
        clear_private(user_id)
        await update.message.reply_text("🔄 Memory cleared! Fresh start — what do you want to learn?")
    else:
        clear_group(chat_id)
        await update.message.reply_text("🔄 Group conversation reset! Let's start fresh 📚")
