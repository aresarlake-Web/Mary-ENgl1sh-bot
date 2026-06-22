"""
Handlers related to chat membership events: welcoming new members and
handling their English-level selection.
"""

import random

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.data.texts import LEVEL_RESPONSES, WELCOME_MESSAGES
from app.keyboards.welcome_keyboard import build_level_keyboard

# Statuses that count as "now an active member"
_ACTIVE_STATUSES = ("member", "administrator")
# Statuses that, if held before, mean this isn't a fresh join
_ALREADY_PRESENT_STATUSES = ("member", "administrator", "creator")


async def on_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome new members when they join the group."""
    result = update.chat_member

    # Only trigger when someone joins
    if result.new_chat_member.status not in _ACTIVE_STATUSES:
        return
    if result.old_chat_member.status in _ALREADY_PRESENT_STATUSES:
        return

    new_user = result.new_chat_member.user
    if new_user.is_bot:
        return

    name = new_user.first_name or "friend"
    welcome = random.choice(WELCOME_MESSAGES).format(name=name)

    await context.bot.send_message(
        chat_id=result.chat.id,
        text=welcome + "\n\n*What's your English level?*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=build_level_keyboard(new_user.id),
    )


async def on_level_select_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle a new member's English-level selection from the welcome message."""
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")
    # format: wlevel_beginner_12345
    if len(parts) < 3 or parts[0] != "wlevel":
        return

    level = parts[1]
    target_user_id = int(parts[2])

    # Only the right user can click their own button
    if query.from_user.id != target_user_id:
        await query.answer("This button is not for you 😄", show_alert=True)
        return

    name = query.from_user.first_name or "friend"
    response = LEVEL_RESPONSES.get(level, "Welcome!")

    await query.edit_message_text(
        f"*{name}* chose: {level.capitalize()} ✅\n\n{response}\n\nFeel free to ask me anything anytime! 🙌",
        parse_mode=ParseMode.MARKDOWN,
    )
