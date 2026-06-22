"""
📚 Mary English — Group Manager Bot
Welcomes members + teaches English in groups.

Entry point: wires up all handlers and starts polling.
"""

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.config import TELEGRAM_BOT_TOKEN, configure_logging, validate_config
from app.handlers.commands import (
    cmd_check,
    cmd_help,
    cmd_lesson,
    cmd_quiz,
    cmd_reset,
    cmd_start,
    cmd_tip,
    cmd_word,
)
from app.handlers.members import on_level_select_group, on_new_member
from app.handlers.messages import handle_message

logger = logging.getLogger(__name__)


def build_application() -> Application:
    """Construct the Telegram Application and register all handlers."""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("quiz", cmd_quiz))
    app.add_handler(CommandHandler("lesson", cmd_lesson))
    app.add_handler(CommandHandler("word", cmd_word))
    app.add_handler(CommandHandler("check", cmd_check))
    app.add_handler(CommandHandler("tip", cmd_tip))
    app.add_handler(CommandHandler("reset", cmd_reset))

    # Welcome new members
    app.add_handler(ChatMemberHandler(on_new_member, ChatMemberHandler.CHAT_MEMBER))

    # Level selection buttons from welcome message
    app.add_handler(CallbackQueryHandler(on_level_select_group, pattern="^wlevel_"))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app


def main() -> None:
    """Configure logging, validate config, build the app, and run polling."""
    configure_logging()
    validate_config()

    print("📚 Mary English Group Bot is starting...")

    app = build_application()

    print("✅ Bot is running! Press Ctrl+C to stop.\n")
    print("📌 To use in a group:")
    print("   1. Add the bot to your group")
    print("   2. Make it an admin (for welcome messages)")
    print("   3. Tag it or reply to its messages\n")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
