"""
Inline keyboards related to the welcome flow.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_level_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Build the 'What's your English level?' inline keyboard for a new member.

    Args:
        user_id: Telegram user id of the new member, embedded in the
            callback_data so only that user's click is accepted.

    Returns:
        InlineKeyboardMarkup with Beginner / Intermediate / Advanced buttons.
    """
    keyboard = [
        [
            InlineKeyboardButton("🌱 I'm a Beginner", callback_data=f"wlevel_beginner_{user_id}"),
            InlineKeyboardButton("📗 Intermediate", callback_data=f"wlevel_intermediate_{user_id}"),
            InlineKeyboardButton("📘 Advanced", callback_data=f"wlevel_advanced_{user_id}"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
